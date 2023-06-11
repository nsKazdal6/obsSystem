import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow,QMessageBox
from PyQt5.uic import loadUi
import pyrebase
import json
import os
import logging
import res

firebaseConfig = {
  "apiKey": "AIzaSyDHmSI9Uc5W9xzDor910wV1vjzjPrzITLw",
  "authDomain": "yazilimtasarimi.firebaseapp.com",
  "databaseURL": "https://yazilimtasarimi-default-rtdb.europe-west1.firebasedatabase.app/",
  "projectId": "yazilimtasarimi",
  "storageBucket": "yazilimtasarimi.appspot.com",
  "messagingSenderId": "945501864153",
  "appId": "1:945501864153:web:72390617dc09e118d97ec8"
};

firebase = pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
storage=firebase.storage()

class FirstScreen(QMainWindow):
    def __init__(self):
        super(FirstScreen,self).__init__()
        loadUi("ui/firstScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnEntry.clicked.connect(self.secondScreen)

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def secondScreen(self):
        secondScreen=SecondScreen()
        widget.addWidget(secondScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SecondScreen(QMainWindow):
    def __init__(self):
        super(SecondScreen,self).__init__()
        loadUi("ui/secondScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnLogin.clicked.connect(self.loginFunction)
        self.btnOne.clicked.connect(self.functionOne)
        self.btnTwo.clicked.connect(self.functionTwo)
        self.btnThree.clicked.connect(self.functionThree)


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def loginFunction(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        chooseTitle = self.chooseTitle.text()

        if not chooseTitle:
            QMessageBox.about(self, "HATA", "Lütfen soldan ilgili alanı seçin.")
            return None
        
        if chooseTitle == "Yönetici":        
            academicians = db.child("users").child("admin").get()
            for user in academicians.each():
                if user.val()["username"] == username and user.val()["password"] == password:
                    userInfo = user.key()
                    answer = QMessageBox.question(self, "GİRİŞ BAŞARILI", "Giriş Başarılı! Ana menüye Devam etmek İster misiniz?",\
                        QMessageBox.Yes | QMessageBox.No)
                    if answer == QMessageBox.Yes:
                        self.navigateToCoordinatorMainScreen()
                    else:
                        self.show()
                    return userInfo
                    
            QMessageBox.about(self, "GİRİŞ BAŞARISIZ", "Giriş Başarısız ya da Böyle Bir Kayıt Yok! Lütfen Tekrar Deneyin.")
            return None
        
        if chooseTitle == "Öğretim Görevlisi - Müdek Denetçisi":        
            academicians = db.child("users").child("academicians").get()
            for user in academicians.each():
                if user.val()["username"] == username and user.val()["password"] == password:
                    userInfo = user.key()
                    answer = QMessageBox.question(self, "GİRİŞ BAŞARILI", "Giriş Başarılı! Ana menüye Devam etmek İster misiniz?",\
                        QMessageBox.Yes | QMessageBox.No)
                    if answer == QMessageBox.Yes:
                        self.navigateToAcademicianMainScreen()
                    else:
                        self.show()
                    return userInfo
                    
            QMessageBox.about(self, "GİRİŞ BAŞARISIZ", "Giriş Başarısız ya da Böyle Bir Kayıt Yok! Lütfen Tekrar Deneyin.")
            return None
        
        if chooseTitle == "Öğrenci":                           
            QMessageBox.about(self, "GİRİŞ BAŞARISIZ", "Bu sayfa daha yapım aşamasında.")
            return None
    
    def functionOne(self):
        self.chooseTitle.setText("Yönetici")
    
    def functionTwo(self):
        self.chooseTitle.setText("Öğretim Görevlisi - Müdek Denetçisi")

    def functionThree(self):
        self.chooseTitle.setText("Öğrenci")

    def navigateToCoordinatorMainScreen(self):
        coordinatorMainScreen = CoordinatorMainScreen()
        coordinatorMainScreen.firstFunction()
        widget.addWidget(coordinatorMainScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def navigateToAcademicianMainScreen(self):
        academicianMainScreen = AcademicianMainScreen()
        widget.addWidget(academicianMainScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CoordinatorMainScreen(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreen,self).__init__()
        loadUi("ui/coordinatorMainScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAddUserPage.clicked.connect(self.academicianAddPage)
        self.btnAddStudent.clicked.connect(self.studentAddPage)
        self.btnAddLessonPage.clicked.connect(self.lessonAddPage)
        

    def firstFunction(self):
        self.btnAddLessonPage.clicked.connect(lambda : self.lessonAddPage())
        
        try:
            academicians = db.child("users").child("academicians").get()
            if academicians is not None:
                academicianKeys = []
                for academician in academicians.each():
                    academicianKeys.append(academician.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in academicianKeys))
                academicianData = json.loads(data)

                info_text = ""
                for academician in academicianData:
                    if 'username' in academician:
                        username = academician['username']

                        academician_info_text = f"Ad Soyad : {username}"
                        info_text += academician_info_text + "\n"
                    else:
                        logging.warning("Missing 'username' key in academician: %s", academician)

                self.listUsers.setText(info_text)
                element_count = len(academicianData)
                self.title4_7.setText(str(element_count))
            else:
                self.listUsers.setText("Herhangi bir kayıt bulunamadı.")
                self.title4_7.setText("0")

        except Exception as e:
            logging.error("Error in firstFunction(): %s", e)
            self.listUsers.setText("Henüz bir kayıt eklenmemiş.")
            self.title4_7.setText("0")

        try:
            academicians = db.child("users").child("students").get()
            if academicians is not None:
                academicianKeys = []
                for academician in academicians.each():
                    academicianKeys.append(academician.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in academicianKeys))
                academicianData = json.loads(data)

                info_text = ""
                for academician in academicianData:
                    if 'username' in academician:
                        username = academician['username']
                        info_text += academician_info_text + "\n"
                    else:
                        logging.warning("Missing 'username' key in academician: %s", academician)

                element_count = len(academicianData)
                self.title4_5.setText(str(element_count))
            else:
                self.title4_5.setText("0")

        except Exception as e:
            logging.error("Error in firstFunction(): %s", e)
            self.title4_5.setText("0")

        try:
            academicians = db.child("lessons").get()
            if academicians is not None:
                academicianKeys = []
                for academician in academicians.each():
                    academicianKeys.append(academician.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in academicianKeys))
                academicianData = json.loads(data)

                info_text = ""
                for academician in academicianData:
                    if 'username' in academician:
                        username = academician['username']
                        info_text += academician_info_text + "\n"
                    else:
                        logging.warning("Missing 'username' key in academician: %s", academician)

                element_count = len(academicianData)
                self.title4_6.setText(str(element_count))
            else:
                self.title4_6.setText("0")

        except Exception as e:
            logging.error("Error in firstFunction(): %s", e)
            self.title4_6.setText("0")


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def lessonAddPage(self):
        coordinatorMainScreenTwo=CoordinatorMainScreenTwo()
        coordinatorMainScreenTwo.firstFunction()
        widget.addWidget(coordinatorMainScreenTwo)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def academicianAddPage(self):
        coordinatorMainScreenTwo=CoordinatorMainScreenThree()
        widget.addWidget(coordinatorMainScreenTwo)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def studentAddPage(self):
        coordinatorMainScreenTwo=CoordinatorMainScreenFour()
        widget.addWidget(coordinatorMainScreenTwo)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CoordinatorMainScreenTwo(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreenTwo,self).__init__()
        loadUi("ui/coordinatorMainScreenTwo.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAddLesson.clicked.connect(self.createLesson)
        self.btnHome.clicked.connect(self.Home)

    def firstFunction(self):
        try:
            lessons = db.child("lessons").get()
            if lessons is not None:
                lessonCodes = []
                for lessoN in lessons.each():
                    lessonCodes.append(lessoN.key())

                info_text = ""
                for LessonName in lessonCodes:
                    academicianLessons = db.child("lessons").child(LessonName).get()
                    if academicianLessons is not None:
                        lessonKeys = []
                        for lesson in academicianLessons.each():
                            lessonKeys.append(lesson.val())

                        data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                        lessonData = json.loads(data)

                        for lessonn in lessonData:
                            if 'lessonName' in lessonn:
                                lessonnamE = lessonn['lessonName']
                                academicianName = lessonn['lessonAcademician']

                                lesson_info_text = f"Ders adı : {lessonnamE}"
                                
                                info_text += lesson_info_text + "\n"
                            else:
                                logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)
                    else:
                        logging.warning("No lessons found for academician: %s", academicianName)
                        
                if info_text:
                    self.listLessons.setText(info_text)
                else:
                    self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)

    def createLesson(self):
        lessonName = self.lineLessonName.text()
        lessonCode = self.lineLessonCode.text()
        lessonYear = self.lineLessonYear.text()
        lessonAcademican = self.lineLessonAcademician.text()
        lessonBranch = self.lineLessonBranch.text()
        
        if not lessonName or not lessonCode or not lessonYear or not lessonAcademican or not lessonBranch:
            QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
            return
        
        data = {"lessonName": lessonName, "lessonCode": lessonCode, "lessonYear": lessonYear, "lessonAcademician": lessonAcademican, "lessonBranch": lessonBranch}
        newUser = db.child("lessons").child(lessonCode).push(data)
        newUserId = newUser["name"]
        lesson_data = db.child("lessons").child(lessonCode).child(newUserId).get().val()
        
        if lesson_data["lessonName"] == lessonName and lesson_data["lessonCode"] == lessonCode and lesson_data["lessonYear"] == lessonYear and lesson_data["lessonAcademician"] == lessonAcademican and lesson_data["lessonBranch"] == lessonBranch:
            QMessageBox.about(self, "Kayıt Ekleme Başarılı", "Kayıt Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Kayıt Ekleme Başarısız", "Kayıt Ekleme Başarısız !")

        try:
            lessons = db.child("lessons").get()
            if lessons is not None:
                lessonCodes = []
                for lessoN in lessons.each():
                    lessonCodes.append(lessoN.key())

                info_text = ""
                for LessonName in lessonCodes:
                    academicianLessons = db.child("lessons").child(LessonName).get()
                    if academicianLessons is not None:
                        lessonKeys = []
                        for lesson in academicianLessons.each():
                            lessonKeys.append(lesson.val())

                        data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                        lessonData = json.loads(data)

                        for lessonn in lessonData:
                            if 'lessonName' in lessonn:
                                lessonnamE = lessonn['lessonName']
                                academicianName = lessonn['lessonAcademician']

                                lesson_info_text = f"Ders adı : {lessonnamE}"
                                
                                info_text += lesson_info_text + "\n"
                            else:
                                logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)
                    else:
                        logging.warning("No lessons found for academician: %s", academicianName)
                        
                if info_text:
                    self.listLessons.setText(info_text)
                else:
                    self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def Home(self):
        coordinatorMainScreenTwo=CoordinatorMainScreen()
        coordinatorMainScreenTwo.firstFunction()
        widget.addWidget(coordinatorMainScreenTwo)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
class CoordinatorMainScreenThree(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreenThree,self).__init__()
        loadUi("ui/coordinatorMainScreenThree.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnHome.clicked.connect(self.Home)
        self.btnAddUser.clicked.connect(self.createUser)

    def createUser(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        name = self.lineName.text()
        mail = self.lineMail.text()
        
        if not username or not password:
             QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
             return
        
        data = {"username": username, "password": password, "name": name, "mail": mail}
        newUser = db.child("users").child("academicians").push(data)
        newUserId = newUser["name"]
        user_data = db.child("users").child("academicians").child(newUserId).get().val()
        
        if user_data["username"] == username and user_data["password"] == password and user_data["name"] == name and user_data["mail"] == mail:
            QMessageBox.about(self, "Kayıt Ekleme Başarılı", "Kayıt Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Kayıt Ekleme Başarısız", "Kayıt Ekleme Başarısız !")


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def Home(self):
        coordinatorMainScreen=CoordinatorMainScreen()
        coordinatorMainScreen.firstFunction()
        widget.addWidget(coordinatorMainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CoordinatorMainScreenFour(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreenFour,self).__init__()
        loadUi("ui/coordinatorMainScreenFour.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnHome.clicked.connect(self.Home)
        self.btnAddUser.clicked.connect(self.createUser)

    def createUser(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        name = self.lineName.text()
        mail = self.lineMail.text()
        
        if not username or not password:
             QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
             return
        
        data = {"username": username, "password": password, "name": name, "mail": mail}
        newUser = db.child("users").child("students").push(data)
        newUserId = newUser["name"]
        user_data = db.child("users").child("students").child(newUserId).get().val()
        
        if user_data["username"] == username and user_data["password"] == password and user_data["name"] == name and user_data["mail"] == mail:
            QMessageBox.about(self, "Kayıt Ekleme Başarılı", "Kayıt Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Kayıt Ekleme Başarısız", "Kayıt Ekleme Başarısız !")

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def Home(self):
        coordinatorMainScreen=CoordinatorMainScreen()
        coordinatorMainScreen.firstFunction()
        widget.addWidget(coordinatorMainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AcademicianMainScreen(QMainWindow):
    def __init__(self):
        super(AcademicianMainScreen,self).__init__()
        loadUi("ui/academicianMainScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAdd.clicked.connect(self.createStudentNotes)

    def createStudentNotes(self):
        studentNumber = self.lineStudentName.text()
        studentName = self.lineStudentNumber.text()
        lessonCode = self.lineLessonCode.text()
        midterm = self.lineMidterm.text()
        final = self.lineFinal.text()
        
        if not studentNumber or not studentName or not lessonCode or not midterm:
            QMessageBox.about(self, "Not Ekleme Başarısız", "Lütfen tüm alanları doldurun.")
            return
        
        data = {"studentNumber": studentNumber, "studentName": studentName, "lessonCode": lessonCode, "midterm": midterm, "final": final}
        newUser = db.child(studentNumber).child(lessonCode).push(data)
        newUserId = newUser["name"]
        lesson_data = db.child(studentNumber).child(lessonCode).child(newUserId).get().val()
        
        if lesson_data["studentNumber"] == studentNumber and lesson_data["studentName"] == studentName and lesson_data["midterm"] == midterm and lesson_data["final"] == final and lesson_data["lessonCode"] == lessonCode:
            QMessageBox.about(self, "Not Ekleme Başarılı", "Not Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Not Ekleme Başarısız", "Not Ekleme Başarısız !")
    

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()


app=QApplication(sys.argv)
mainwindow=FirstScreen()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.showFullScreen()
app.exec_()