from datetime import datetime
from domain.note import Note

MENU = [
     "1. Create a new note", 
     "2. View all notes", 
     "3. View note by ID", 
     "4. Delete all notes", 
     "5. Delete note by ID",
     "6. Edit a note",
     "0. To exit the app"
]
filename = datetime.now().date()
PATH =f"notes/{filename}.csv"


def startup(fileName: str):  
     """
     This starts up all engines
     """
     PLAY = True
     while PLAY:
       print("SELECT AN OPTION TO PROCEED")
       for i in range (0, len(MENU)):
          print(MENU[i])

       userChoice = int(input("What is your option: "))

       match userChoice:
        case 1:
              create_note(input("Enter your text: "))
        case 2:
              view_all_notes()
        case 3:
              id = int(input("What is the Id of the Note: "))
              note = view_note_by_id(id)

              if note:
                  print(f"ID={note.id} TEXT={note.text}")
        case 4: 
               clear_all()
               print("All notes cleared")        
        case 5:
             id = int(input("What is the Id of the Note: "))
             delete_note_by_id(id)
        case 6:
             id = int(input("What is the Id of the Note: "))
             edit_note_by_id(id)
        case 0:
             PLAY = False
        case _:
                print("Follow the Instructions")
     separator()     


def separator():
    print("                          ")
    print("==========================")
def _setup_all_files():
     import os
     
     if os.path.exists(PATH):
          return
     
     # Create only the 'notes' folder
     os.makedirs(os.path.dirname(PATH), exist_ok=True)
     
     # Now you are ready to actually create the file
     with open (PATH,"x") as f:
         f.write("ID, TEXT\n")
    

def view_all_notes():
     store = get_notes()
     for note in store:
         print(f"ID={note.id} TEXT={note.text}")


def deserealize(input: str):
     if input.endswith('\n'):
        input = input.replace("\n", "")
     array = input.split(',')
     return convert_to_class(array[0], array[1])

def convert_to_class(id: str, text: str) -> Note:
    return Note(int(id), text)  


def serealize(note: Note):
    return f"{note.id},{note.text}\n"

def create_note(text: str) -> str:
    store = get_notes()
    Id = len(store) +1
    note = Note(Id, text)
    store.append(note)
    overwrite(store)
    print("Note was created successfully")


def get_notes() -> list[Note]:
    store : list[Note] = []
    with open(PATH, 'r') as file:
        allLines = file.readlines()
        for i in range(1, len(allLines)):
            store.append(deserealize(allLines[i]))
    return store


def serealize_all_notes(notes: list[Note]) -> list[str]:
    serealized_notes = []
    for note in notes:
        serealized_notes.append(serealize(note))

    return serealized_notes
    

def overwrite(contents: list[Note]):
     with open (PATH,"w") as f:
         f.write("ID, TEXT\n")
         f.writelines(serealize_all_notes(contents))


def clear_all():
     with open (PATH,"w") as f:
         f.write("ID, TEXT\n")


def view_note_by_id(id: int) -> Note:
    store = get_notes()
    for note in store:
        if note.id == id:
            return note
    print("A note with that Id not found")
    return


def delete_note_by_id(id: int):
    store = get_notes()
    for note in store:
        if note.id == id:
            store.remove(note)
            overwrite(store)
            print("Note was successfully deleted")


def edit_note_by_id(id: int):
    store = get_notes()
    for note in store:
        if note.id == id:
            newText = input("What is the new text: ")
            note.text = newText
            overwrite(store)
            print ("Note was edited successfully")
            return

    print("A note with that Id was not found")                


if __name__ == "__main__":
    startup(PATH)       