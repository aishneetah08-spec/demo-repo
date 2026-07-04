"""
FileManager Module for Terminal QuizMaster
Handles all CSV file operations with comprehensive error handling.
"""

import csv
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from exceptions.file_exceptions import (
    PermissionError,
    ValidationError,
    DuplicateEntryError,
    FileCorruptedError,
    FileNotFoundError,
    FileManagerError,
)
from enums import UserRole, QuestionType


class FileManager:
    """
    Utility class for handling CSV file operations with comprehensive error handling.
    Uses static methods to provide a centralized interface for data persistence.
    """

    # File paths
    USERS_FILE = "users.csv"
    QUESTIONS_FILE = "questions.csv"
    RESULTS_FILE = "results.csv"

    # CSV Headers
    USERS_HEADERS = ["id", "username", "password", "role"]
    QUESTIONS_HEADERS = ["id", "type", "text", "options", "answer", "difficulty"]
    RESULTS_HEADERS = ["student_id", "score", "total_questions", "date"]

    # Validation constants
    MAX_USERNAME_LENGTH = 50
    MAX_PASSWORD_LENGTH = 128
    MIN_PASSWORD_LENGTH = 6
    MAX_QUESTION_LENGTH = 500
    MAX_DIFFICULTY = 5
    MIN_DIFFICULTY = 1

    # Configure logging
    _logger = None

    @staticmethod
    def _get_logger() -> logging.Logger:
        """
        Get or create a logger instance.

        Returns:
            Configured logger instance
        """
        if FileManager._logger is None:
            FileManager._logger = logging.getLogger("FileManager")
            FileManager._logger.setLevel(logging.INFO)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Create file handler
            try:
                file_handler = logging.FileHandler("quizmaster.log")
                file_handler.setLevel(logging.DEBUG)

                # Create formatter
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                console_handler.setFormatter(formatter)
                file_handler.setFormatter(formatter)

                # Add handlers
                FileManager._logger.addHandler(console_handler)
                FileManager._logger.addHandler(file_handler)
            except Exception as e:
                # If file handler fails, continue with console only
                console_handler.setFormatter(
                    logging.Formatter("%(levelname)s - %(message)s")
                )
                FileManager._logger.addHandler(console_handler)
                FileManager._logger.warning(f"Could not create file handler: {e}")

        return FileManager._logger

    @staticmethod
    def initialize_files() -> None:
        """
        Initialize all CSV files with headers if they don't exist.
        Called at application startup.

        Raises:
            PermissionError: If files cannot be created due to permissions
            FileManagerError: If file initialization fails
        """
        logger = FileManager._get_logger()

        try:
            logger.info("Initializing CSV files...")

            FileManager._create_file_if_not_exists(
                FileManager.USERS_FILE, FileManager.USERS_HEADERS
            )
            FileManager._create_file_if_not_exists(
                FileManager.QUESTIONS_FILE, FileManager.QUESTIONS_HEADERS
            )
            FileManager._create_file_if_not_exists(
                FileManager.RESULTS_FILE, FileManager.RESULTS_HEADERS
            )

            logger.info("CSV files initialized successfully")

        except OSError as e:
            logger.error(f"Permission error during file initialization: {e}")
            raise PermissionError(f"Cannot create files. Check permissions: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error during file initialization: {e}")
            raise FileManagerError(f"File initialization failed: {e}") from e

    @staticmethod
    def _create_file_if_not_exists(filename: str, headers: List[str]) -> None:
        """
        Create a CSV file with headers if it doesn't exist.

        Args:
            filename: Name of the CSV file
            headers: List of column headers

        Raises:
            ValidationError: If headers are invalid
            PermissionError: If file cannot be created
        """
        logger = FileManager._get_logger()

        # Validate headers
        if not headers or not all(isinstance(h, str) for h in headers):
            raise ValidationError(f"Invalid headers for {filename}")

        if os.path.exists(filename):
            logger.debug(f"{filename} already exists, skipping creation")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            logger.info(f"Created {filename} with headers")

        except OSError as e:
            logger.error(f"Permission error creating {filename}: {e}")
            raise PermissionError(f"Cannot create {filename}: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error creating {filename}: {e}")
            raise FileManagerError(f"Failed to create {filename}: {e}") from e

    @staticmethod
    def _validate_file_integrity(filename: str, expected_headers: List[str]) -> bool:
        """
        Validate that a CSV file has the correct headers.

        Args:
            filename: Name of the CSV file
            expected_headers: Expected column headers

        Returns:
            True if file is valid

        Raises:
            FileCorruptedError: If file headers don't match
        """
        logger = FileManager._get_logger()

        try:
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                actual_headers = next(reader, None)

                if actual_headers != expected_headers:
                    logger.error(
                        f"{filename} has incorrect headers. "
                        f"Expected: {expected_headers}, Got: {actual_headers}"
                    )
                    raise FileCorruptedError(
                        f"{filename} is corrupted or has invalid format"
                    )

            return True

        except StopIteration:
            raise FileCorruptedError(f"{filename} is empty or corrupted")
        except Exception as e:
            logger.error(f"Error validating {filename}: {e}")
            raise

    @staticmethod
    def read_csv(filename: str, validate: bool = True) -> List[Dict[str, str]]:
        """
        Read a CSV file and return data as a list of dictionaries.
        Each dictionary represents a row with headers as keys.

        Args:
            filename: Name of the CSV file to read
            validate: Whether to validate file integrity

        Returns:
            List of dictionaries representing rows

        Raises:
            FileNotFoundError: If file doesn't exist
            FileCorruptedError: If file is corrupted
            FileManagerError: For other read errors

        Example:
            [{'id': '1', 'username': 'admin', 'password': 'pass', 'role': 'admin'}]
        """
        logger = FileManager._get_logger()
        data = []

        if not os.path.exists(filename):
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(f"{filename} does not exist")

        # Validate file integrity
        if validate:
            if filename == FileManager.USERS_FILE:
                FileManager._validate_file_integrity(
                    filename, FileManager.USERS_HEADERS
                )
            elif filename == FileManager.QUESTIONS_FILE:
                FileManager._validate_file_integrity(
                    filename, FileManager.QUESTIONS_HEADERS
                )
            elif filename == FileManager.RESULTS_FILE:
                FileManager._validate_file_integrity(
                    filename, FileManager.RESULTS_HEADERS
                )

        try:
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row_num, row in enumerate(
                    reader, start=2
                ):  # start=2 because row 1 is header
                    # Validate row has data
                    if not any(row.values()):
                        logger.warning(f"Empty row at line {row_num} in {filename}")
                        continue

                    data.append(row)

            logger.debug(f"Successfully read {len(data)} records from {filename}")
            return data

        except csv.Error as e:
            logger.error(f"CSV format error in {filename}: {e}")
            raise FileCorruptedError(f"{filename} has invalid CSV format: {e}") from e
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in {filename}: {e}")
            raise FileCorruptedError(f"{filename} has encoding issues: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error reading {filename}: {e}")
            raise FileManagerError(f"Failed to read {filename}: {e}") from e

    @staticmethod
    def append_to_csv(filename: str, data: Dict[str, Any]) -> bool:
        """
        Append a new row to a CSV file.

        Args:
            filename: Name of the CSV file
            data: Dictionary with column names as keys

        Returns:
            True if successful

        Raises:
            FileNotFoundError: If file doesn't exist
            ValidationError: If data is invalid
            FileManagerError: For other write errors
        """
        logger = FileManager._get_logger()

        if not os.path.exists(filename):
            logger.error(f"Cannot append to non-existent file: {filename}")
            raise FileNotFoundError(f"{filename} does not exist")

        # Validate data
        if not data or not isinstance(data, dict):
            raise ValidationError("Data must be a non-empty dictionary")

        try:
            # Read headers from the file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)

            # Validate all required headers are present in data
            for header in headers:
                if header not in data:
                    logger.warning(
                        f"Missing field '{header}' in data, using empty string"
                    )
                    data[header] = ""

            # Append the new row
            with open(filename, "a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(data)

            logger.info(f"Successfully appended data to {filename}")
            return True

        except OSError as e:
            logger.error(f"Permission error writing to {filename}: {e}")
            raise PermissionError(f"Cannot write to {filename}: {e}") from e
        except csv.Error as e:
            logger.error(f"CSV error writing to {filename}: {e}")
            raise FileManagerError(f"CSV write error in {filename}: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error appending to {filename}: {e}")
            raise FileManagerError(f"Failed to append to {filename}: {e}") from e

    @staticmethod
    def get_next_id(filename: str) -> int:
        """
        Get the next available ID for a CSV file.
        Useful for auto-incrementing primary keys.

        Args:
            filename: Name of the CSV file

        Returns:
            Next available ID (1 if file is empty)

        Raises:
            FileManagerError: If ID calculation fails
        """
        logger = FileManager._get_logger()

        try:
            data = FileManager.read_csv(filename, validate=False)

            if not data:
                logger.debug(f"No existing records in {filename}, returning ID 1")
                return 1

            # Find the maximum existing ID
            max_id = 0
            for row in data:
                try:
                    current_id = int(row.get("id", 0))
                    if current_id > max_id:
                        max_id = current_id
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid ID in {filename}: {row.get('id')} - {e}")
                    continue

            next_id = max_id + 1
            logger.debug(f"Next ID for {filename}: {next_id}")
            return next_id

        except Exception as e:
            logger.error(f"Error calculating next ID for {filename}: {e}")
            raise FileManagerError(f"Failed to calculate next ID: {e}") from e

    @staticmethod
    def _validate_username(username: str) -> None:
        """
        Validate username format.

        Args:
            username: Username to validate

        Raises:
            ValidationError: If username is invalid
        """
        if not username or not isinstance(username, str):
            raise ValidationError("Username must be a non-empty string")

        if len(username) > FileManager.MAX_USERNAME_LENGTH:
            raise ValidationError(
                f"Username exceeds maximum length of {FileManager.MAX_USERNAME_LENGTH}"
            )

        if not username.strip():
            raise ValidationError("Username cannot be only whitespace")

        # Check for invalid characters
        invalid_chars = [",", "\n", "\r", '"', "'"]
        if any(char in username for char in invalid_chars):
            raise ValidationError(
                f"Username contains invalid characters: {invalid_chars}"
            )

    @staticmethod
    def _validate_password(password: str) -> None:
        """
        Validate password format.

        Args:
            password: Password to validate

        Raises:
            ValidationError: If password is invalid
        """
        if not password or not isinstance(password, str):
            raise ValidationError("Password must be a non-empty string")

        if len(password) < FileManager.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password must be at least {FileManager.MIN_PASSWORD_LENGTH}"
                "characters"
            )

        if len(password) > FileManager.MAX_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password exceeds maximum length of {FileManager.MAX_PASSWORD_LENGTH}"
            )

    @staticmethod
    def _validate_role(role: str) -> None:
        """
        Validate user role.

        Args:
            role: Role to validate

        Raises:
            ValidationError: If role is invalid
        """
        valid_roles = [r.value for r in UserRole]
        if role.lower() not in valid_roles:
            raise ValidationError(
                f"Invalid role '{role}'. Must be one of: {valid_roles}"
            )

    @staticmethod
    def find_user(username: str) -> Optional[Dict[str, str]]:
        """
        Find a user by username.

        Args:
            username: Username to search for

        Returns:
            Dictionary with user data if found, None otherwise

        Raises:
            ValidationError: If username is invalid
            FileManagerError: If file read fails
        """
        logger = FileManager._get_logger()

        try:
            FileManager._validate_username(username)

            users = FileManager.read_csv(FileManager.USERS_FILE)

            for user in users:
                if user["username"].lower() == username.lower():
                    logger.debug(f"User found: {username}")
                    return user

            logger.debug(f"User not found: {username}")
            return None

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error finding user {username}: {e}")
            raise FileManagerError(f"Failed to find user: {e}") from e

    @staticmethod
    def get_questions_by_type(
        question_type: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Get all questions, optionally filtered by type.

        Args:
            question_type: Type of questions to filter ('mcq' or 'tf'), None for all

        Returns:
            List of question dictionaries

        Raises:
            ValidationError: If question_type is invalid
            FileManagerError: If file read fails
        """
        logger = FileManager._get_logger()

        try:
            # Validate question type if provided
            if question_type:
                valid_types = [qt.value for qt in QuestionType]
                if question_type.lower() not in valid_types:
                    raise ValidationError(
                        f"Invalid question type '{question_type}'. Must be one of: "
                        "{valid_types}"
                    )

            questions = FileManager.read_csv(FileManager.QUESTIONS_FILE)

            if question_type:
                filtered = [
                    q for q in questions if q["type"].lower() == question_type.lower()
                ]
                logger.debug(f"Found {len(filtered)} questions of type {question_type}")
                return filtered

            logger.debug(f"Found {len(questions)} total questions")
            return questions

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error getting questions: {e}")
            raise FileManagerError(f"Failed to get questions: {e}") from e

    @staticmethod
    def get_student_results(student_id: int) -> List[Dict[str, str]]:
        """
        Get all quiz results for a specific student.

        Args:
            student_id: ID of the student

        Returns:
            List of result dictionaries

        Raises:
            ValidationError: If student_id is invalid
            FileManagerError: If file read fails
        """
        logger = FileManager._get_logger()

        try:
            if not isinstance(student_id, int) or student_id < 1:
                raise ValidationError("Student ID must be a positive integer")

            results = FileManager.read_csv(FileManager.RESULTS_FILE)
            student_results = [r for r in results if r["student_id"] == str(student_id)]

            logger.debug(
                f"Found {len(student_results)} results for student {student_id}"
            )
            return student_results

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error getting results for student {student_id}: {e}")
            raise FileManagerError(f"Failed to get student results: {e}") from e

    @staticmethod
    def get_all_results_sorted() -> List[Dict[str, str]]:
        """
        Get all quiz results sorted by score (descending).
        Useful for leaderboards.

        Returns:
            Sorted list of result dictionaries

        Raises:
            FileManagerError: If file read or sort fails
        """
        logger = FileManager._get_logger()

        try:
            results = FileManager.read_csv(FileManager.RESULTS_FILE)

            # Sort by score (descending), then by date (most recent first)
            def sort_key(result):
                try:
                    score = int(result.get("score", 0))
                    date = result.get("date", "")
                    return (score, date)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid result data: {result}")
                    return (0, "")

            results.sort(key=sort_key, reverse=True)
            logger.debug(f"Sorted {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error getting sorted results: {e}")
            raise FileManagerError(f"Failed to get sorted results: {e}") from e

    @staticmethod
    def save_quiz_result(student_id: int, score: int, total_questions: int) -> bool:
        """
        Save a quiz result for a student.

        Args:
            student_id: ID of the student
            score: Score achieved
            total_questions: Total number of questions

        Returns:
            True if successful

        Raises:
            ValidationError: If data is invalid
            FileManagerError: If save fails
        """
        logger = FileManager._get_logger()

        try:
            # Validate inputs
            if not isinstance(student_id, int) or student_id < 1:
                raise ValidationError("Student ID must be a positive integer")

            if not isinstance(score, int) or score < 0:
                raise ValidationError("Score must be a non-negative integer")

            if not isinstance(total_questions, int) or total_questions < 1:
                raise ValidationError("Total questions must be a positive integer")

            if score > total_questions:
                raise ValidationError("Score cannot exceed total questions")

            result_data = {
                "student_id": str(student_id),
                "score": str(score),
                "total_questions": str(total_questions),
                "date": datetime.now().strftime("%Y-%m-%d"),
            }

            success = FileManager.append_to_csv(FileManager.RESULTS_FILE, result_data)

            if success:
                logger.info(
                    f"Saved result for student {student_id}: "
                    f"{score}/{total_questions}"
                )

            return success

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error saving quiz result: {e}")
            raise FileManagerError(f"Failed to save quiz result: {e}") from e

    @staticmethod
    def add_user(username: str, password: str, role: str) -> bool:
        """
        Add a new user to the system.

        Args:
            username: Username for the new user
            password: Password (should already be hashed/processed)
            role: 'admin' or 'student'

        Returns:
            True if successful

        Raises:
            ValidationError: If input data is invalid
            DuplicateEntryError: If username already exists
            FileManagerError: If save fails
        """
        logger = FileManager._get_logger()

        try:
            # Validate inputs
            FileManager._validate_username(username)
            FileManager._validate_password(password)
            FileManager._validate_role(role)

            # Check if username already exists
            if FileManager.find_user(username):
                logger.warning(f"Attempted to create duplicate user: {username}")
                raise DuplicateEntryError(f"Username '{username}' already exists")

            user_id = FileManager.get_next_id(FileManager.USERS_FILE)

            user_data = {
                "id": str(user_id),
                "username": username,
                "password": password,
                "role": role.lower(),
            }

            success = FileManager.append_to_csv(FileManager.USERS_FILE, user_data)

            if success:
                logger.info(f"Created new user: {username} (role: {role})")

            return success

        except (ValidationError, DuplicateEntryError):
            raise
        except Exception as e:
            logger.error(f"Error adding user {username}: {e}")
            raise FileManagerError(f"Failed to add user: {e}") from e

    @staticmethod
    def add_question(
        question_type: str, text: str, options: str, answer: str, difficulty: int
    ) -> bool:
        """
        Add a new question to the question bank.

        Args:
            question_type: 'mcq' or 'tf'
            text: Question text
            options: Pipe-separated options for MCQ, empty for True/False
            answer: Correct answer
            difficulty: Difficulty level (1-5)

        Returns:
            True if successful

        Raises:
            ValidationError: If input data is invalid
            FileManagerError: If save fails
        """
        logger = FileManager._get_logger()

        try:
            # Validate question type
            valid_types = [qt.value for qt in QuestionType]
            if question_type.lower() not in valid_types:
                raise ValidationError(
                    f"Invalid question type '{question_type}'."
                    "Must be one of: {valid_types}"
                )

            # Validate text
            if not text or not isinstance(text, str):
                raise ValidationError("Question text must be a non-empty string")

            if len(text) > FileManager.MAX_QUESTION_LENGTH:
                raise ValidationError(
                    f"Question text exceeds maximum length of {FileManager.MAX_QUESTION_LENGTH}"
                )

            # Validate difficulty
            if not isinstance(difficulty, int):
                raise ValidationError("Difficulty must be an integer")

            if (
                difficulty < FileManager.MIN_DIFFICULTY
                or difficulty > FileManager.MAX_DIFFICULTY
            ):
                raise ValidationError(
                    f"Difficulty must be between {FileManager.MIN_DIFFICULTY} "
                    f"and {FileManager.MAX_DIFFICULTY}"
                )

            # Validate MCQ-specific requirements
            if question_type.lower() == QuestionType.MCQ.value:
                if not options or "|" not in options:
                    raise ValidationError(
                        "MCQ questions must have pipe-separated options (e.g., 'A|B|C|D')"
                    )

                option_list = [opt.strip() for opt in options.split("|")]
                if len(option_list) < 2:
                    raise ValidationError("MCQ questions must have at least 2 options")

                if answer not in option_list:
                    raise ValidationError(
                        f"Answer '{answer}' must be one of the options: {option_list}"
                    )

            # Validate True/False specific requirements
            if question_type.lower() == QuestionType.TRUE_FALSE.value:
                valid_answers = ["True", "False", "true", "false", "T", "F"]
                if answer not in valid_answers:
                    raise ValidationError(
                        f"True/False answer must be one of: {valid_answers}"
                    )

            # Validate answer
            if not answer or not isinstance(answer, str):
                raise ValidationError("Answer must be a non-empty string")

            question_id = FileManager.get_next_id(FileManager.QUESTIONS_FILE)

            question_data = {
                "id": str(question_id),
                "type": question_type.lower(),
                "text": text.strip(),
                "options": options.strip(),
                "answer": answer.strip(),
                "difficulty": str(difficulty),
            }

            success = FileManager.append_to_csv(
                FileManager.QUESTIONS_FILE, question_data
            )

            if success:
                logger.info(
                    f"Added question (ID: {question_id}, Type: {question_type}, "
                    f"Difficulty: {difficulty})"
                )

            return success

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error adding question: {e}")
            raise FileManagerError(f"Failed to add question: {e}") from e

