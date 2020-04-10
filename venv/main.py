import time,unittest
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class Full_e2e_test(unittest.TestCase):#наследует
    @classmethod
    def setUpClass(cls,browser = input('Какой браузер:')):
        global inf
        if browser == 'Opera':
            cls.driver = webdriver.Opera(executable_path=r'C:\Users\Павел\PycharmProjects\testing_work_task\operadriver.exe')
            cls.driver.maximize_window()
            cls.driver.get('http://91.217.196.36:5000/')
            cls.driver.implicitly_wait(4)
            inf = 'Opera'
        if browser == 'Chrome':
            cls.driver = webdriver.Chrome(executable_path=r'')
            cls.driver.get('http://91.217.196.36:5000/')
            cls.driver.implicitly_wait(4)
            inf = 'Chrome'
        if browser == 'Firefox':
            cls.driver = webdriver.Firefox(executable_path=r'')
            cls.driver.get('http://91.217.196.36:5000/')
            cls.driver.implicitly_wait(4)
            inf = 'Firefox'
    def test01(self):
        """проверка кномпки Add Todo,кнопки Close"""
        driver = self.driver
        names = ['make to-do list', 'try-edit','scratch this','#close#']
        for i in names:
            add_todo_btn = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[1]/button[1]').click()
            driver.implicitly_wait(10)
            input_field = driver.find_element_by_xpath("//input[@class='input']").send_keys(i)
            driver.implicitly_wait(10)
            if i == '#close#':
                button_close = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[1]').click()
            else:
                button_save = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[2]').click()
            driver.implicitly_wait(10)
        todo_list = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[2]/div[2]/table').text
        time.sleep(3)
        element = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[2]/div[2]/table/tbody')
        element.screenshot("{}_'make to-do list'.'try-edit'.'scratch this'.png".format(inf))
        assert '#close#' not in todo_list  # утверждаю '#close#' нет в todo листе
    def test02(self):
        """проверка выставления приоритета"""
        driver = self.driver
        names = ['buy milk','try to live','to sleep']
        n=1
        for i in names:
            add_todo_btn = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[1]/button[1]').click()
            driver.implicitly_wait(10)
            input_field = driver.find_element_by_xpath("//input[@class='input']").send_keys(i)
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("//span[@class='select']").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/section/div[2]/div/span/select/option[{}]'.format(n)).click()
            driver.implicitly_wait(10)
            button_save = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[2]').click()
            n+=1
            driver.implicitly_wait(10)
            time.sleep(1)
        todo_list = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[2]/div[2]/table/tbody').text
        assert 'secondary' and 'important' and 'meh' in todo_list
        driver.save_screenshot("{}_priority-important_meh_secondary.png".format(inf))

    def test03(self):
        """сортировка по id"""
        driver = self.driver
        driver.find_element_by_class_name('is-sortable').click()
        driver.implicitly_wait(10)

        driver.find_element_by_class_name('is-sortable').click()
        driver.implicitly_wait(10)

        driver.find_element_by_class_name('is-sortable').click()
        driver.implicitly_wait(10)
        true_list=['1','2','3','4','5','6']
        id_list=[]
        for i in range(6):
            id = driver.find_elements_by_xpath("//td[@data-label='ID']")[i].text
            id_list.append(id)
        time.sleep(1)
        #print(id_list)
        driver.save_screenshot("{}_id_1_to_6.png".format(inf))
        assert id_list == true_list,('Сортировка по id неверна')


    def test04(self):
        """сортировка по названиям"""
        driver = self.driver
        driver.find_elements_by_class_name('is-sortable')[1].click()
        time.sleep(1)
        driver.find_elements_by_class_name('is-sortable')[1].click()
        time.sleep(1)
        true_list = ['try-edit', 'try to live', 'to sleep', 'scratch this', 'make to-do list', 'buy milk']
        todo_list=[]
        for i in range(6):
            id = driver.find_elements_by_xpath("//td[@data-label='Todo']")[i].text
            todo_list.append(id)
            time.sleep(.5)
        element = driver.find_element_by_xpath('//*[@id="app"]/div')
        element.screenshot("{}_try-edit.try to live.to sleep.scratch this.make to-do list.buy milk'.png".format(inf))
        assert todo_list == true_list, ('Сортировка по Названиям неверна')

    def test05(self):
        """редактирование заголовка"""
        driver = self.driver
        true_list = ['try-edit+rename', 'try to live+rename', 'to sleep+rename', 'scratch this+rename',
                     'make to-do list+rename', 'buy milk+rename']
        todo_list = []
        for i in range(6):#!!!пусть поменяет статус у 6.
            driver.find_elements_by_xpath("//i[@class='mdi mdi-settings-outline']")[i].click()
            driver.implicitly_wait(20)
            input_field = driver.find_element_by_xpath("//input[@class='input']").send_keys('+rename')
            driver.implicitly_wait(20)
            button_save = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[2]').click()
            driver.implicitly_wait(20)

        for i in range(6):
            id = driver.find_elements_by_xpath("//td[@data-label='Todo']")[i].text
            todo_list.append(id)
            time.sleep(1)
        driver.save_screenshot("{}_titlesRename.png".format(inf))
        #print(todo_list)
        assert todo_list == true_list, ('Редактирование заголовка не работает')

    def test06(self):
        """редактирование приоритета"""
        driver = self.driver
        true_list = ['important', 'important', 'important', 'important', 'important', 'important']
        todo_list = []
        for i in range(6):#!!!пусть поменяет статус у 6.
            driver.find_elements_by_xpath("//i[@class='mdi mdi-settings-outline']")[i].click()
            #print('у меня',len(l))
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("//span[@class='select']").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div/section/div[2]/div/span/select/option[2]').click()
            driver.implicitly_wait(10)
            button_save = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[2]').click()
            driver.implicitly_wait(10)
        for i in range(6):
            id = driver.find_elements_by_xpath("//td[@data-label='Priority']")[i].text
            todo_list.append(id)
            time.sleep(.5)
        #print(todo_list)
        element = driver.find_element_by_xpath('//*[@id="app"]/div')
        element.screenshot("{}_important.important.important.important.important.important.png".format(inf))
        assert todo_list == true_list, ('Редактирование приоритета не работает')

    def test07(self):
        """сортировка по приороитету"""
        driver = self.driver
        driver.find_elements_by_class_name('is-sortable')[2].click()
        #driver.implicitly_wait(10)

        # driver.find_element_by_class_name('is-sortable').click()
        # driver.implicitly_wait(10)
        #
        # driver.find_element_by_class_name('is-sortable').click()
        # driver.implicitly_wait(10)
        true_list = ['important', 'meh', 'secondary', '', '', '']
        todo_list = []
        for i in range(6):
            p = driver.find_elements_by_xpath("//td[@data-label='Priority']")[i].text
            todo_list.append(p)
        #print('Сорт приоритета:',todo_list)
        driver.save_screenshot("{}_'important.'meh'.'secondary'.png".format(inf))
        assert todo_list == true_list, ('Сортировка по приоритету неверна')
    # @classmethod
    # def tearDown(cls):
    #     cls.driver.quit()
    def test08(self):
        """удалить запись"""
        driver = self.driver
        true_list = ['make to-do list+rename', 'try-edit+rename', 'scratch this+rename']
        todo_list = []
        for i in range(3):
            driver.find_element_by_xpath("//i[@class='mdi mdi-delete']").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("//button[@class='button is-danger']").click()
            driver.implicitly_wait(10)
        for i in range(3):
            id = driver.find_elements_by_xpath("//td[@data-label='Todo']")[i].text
            todo_list.append(id)
            time.sleep(.5)
        driver.save_screenshot("{}'make to-do list+rename'.'try-edit+rename'.'scratch this+rename'.png".format(inf))
        #print('Del',todo_list)
        assert todo_list == true_list, ('Удаление не работает,или некорректно')
    def test09(self):
        """кнопка Delete all"""
        driver = self.driver
        driver.find_element_by_xpath('// *[ @ id = "app"] / div / section / div / div[1] / button[2]').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//button[@class='button is-danger']").click()
        driver.save_screenshot("{}_'пустая таблица'.png".format(inf))
        assert driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[2]/div[2]/table/tbody/tr'),\
            ('Кнопка удалить всё не работает')

    def test10(self):
        """Todo без названия"""
        driver = self.driver
        add_todo_btn = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[1]/button[1]').click()
        driver.implicitly_wait(10)
        time.sleep(3)
        input_field = driver.find_element_by_xpath("//input[@class='input']").send_keys(' ')
        driver.implicitly_wait(10)
        time.sleep(3)

        button_save = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/footer/button[2]').click()
        time.sleep(3)

        driver.save_screenshot("{}_'пустая таблица,без id 1'.png".format(inf))
        obj = driver.find_element_by_xpath("//td[@data-label='ID']").text
        assert obj is None,('Объект создается без названия')
if __name__ == '__main__':
    unittest.main()