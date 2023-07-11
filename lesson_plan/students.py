

class student:
    def __init__(self):
        self._board=""
        self._std=""
        self._subject=""
        self._subsubject=""
        self._lesson=""
        self._subtopic="All"
        self._mode="Learning"
    
    def Display(self):
        return f"Generating Plan for {self.std} {self.subject} subject for student of {self.board}"
    
    #setter methods:
    def set_board(self,board):
        self._board=board
    
    def set_std(self,std):
        self._std=std

    def set_subject(self,subject):
        self._subject=subject

    def set_subsubject(self,subsubject):
        self._subsubject=subsubject
    
    def set_lesson(self,lesson):
        self._lesson=lesson

    def set_board(self,mode):
        self._mode=mode
    def set_subtopic(self,subtopic):
        self._subtopic=subtopic

    #getter methods
    def get_board(self):
        return self._board
    
    def get_std(self):
        return self._std

    def get_subject(self):
        return self._subject

    def get_subsubject(self):
        return self._subsubject
    
    def get_lesson(self):
        return self._lesson

    def get_board(self):
        return self._mode
    def get_subtopic(self):
        return self._subtopic

    