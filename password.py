import PySimpleGUI as sg
import hashlib
import pygame

def main():
    def HashGeneratorGUI():
        layout = [
            [sg.Text('Password Hash Generator', size=(30, 1), font='Any 15')],
            [sg.Text('Password'), sg.Input(key='-password-')],
            [sg.Text('SHA Hash'), sg.Input('', size=(40, 1), key='hash')],
        ]

        window = sg.Window('SHA Generator', layout,
                           auto_size_text=False,
                           default_element_size=(10, 1),
                           text_justification='r',
                           return_keyboard_events=True,
                           grab_anywhere=False)

        while True:
            event, values = window.read()
            if event is None:
                break

            password = values['-password-']
            try:
                password_utf = password.encode('utf-8')
                sha1hash = hashlib.sha1()
                sha1hash.update(password_utf)
                password_hash = sha1hash.hexdigest()
                window['hash'].update(password_hash)
            except:
                pass
        window.close()
   
    def PasswordMatches(password, a_hash):
        password_utf = password.encode('utf-8')
        sha1hash = hashlib.sha1()
        sha1hash.update(password_utf)
        password_hash = sha1hash.hexdigest()
        return password_hash == a_hash

    login_password_hash = '549cdd460d3d98e518f58fd09c1d50afaacde4a7'
    password = sg.popup_get_text(
        'Password: (Password behind screen)', password_char='*')
    if password == 'gui':                   
        HashGeneratorGUI()                             
        return                                         
    if password and PasswordMatches(password, login_password_hash):
        
        pygame.init()

        white = (255, 255, 255)

        X = 1600
        Y = 900

        display_surface = pygame.display.set_mode((X, Y ))

        pygame.display.set_caption('Image')
        image = pygame.image.load('skattkarta.png')

        while True :
            display_surface.fill((0,128,128))
            display_surface.blit(image, (575, 0))
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()

                pygame.display.update()         
        
    else:
        print('Login FAILED!!')


if __name__ == '__main__':
    sg.change_look_and_feel('DarkAmber')
    main()
