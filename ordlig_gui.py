from typing import List
import PySimpleGUI as sg
from findWord import findWords, openDictionary, create_correct_letter, correct_letter

def check_illegal_input_values(cor_pos, cor, not_contain) -> bool:
    legal_values = cor_pos + cor
    for letter in legal_values:
        if letter in not_contain:
            return True
    return False

def clean_input_line(values):
    temp = ''
    letter :str 
    for letter in values:
        if letter.isalpha():
            temp = temp + letter.lower()
    return ''.join(sorted(list(set(temp))))

def main():
    correct_pos_names        = ['first_pos','second_pos','third_pos','fourth_pos','fifth_pos']
    contains_letter_name     = 'contain_letters'
    not_contains_letter_name = 'not_contains'

    nb_dictionary = openDictionary('fem_bokstav.txt')
    # All the stuff inside your window.
    layout = [  [sg.Titlebar('Ordlig', background_color='grey')],
                [sg.Text('Riktige bokstaver rett plass'), 
                sg.Input(size=1, enable_events=True, key='first_pos'),
                sg.Input(size=1, enable_events=True, key='second_pos'),
                sg.Input(size=1, enable_events=True, key='third_pos'),
                sg.Input(size=1, enable_events=True, key='fourth_pos'),
                sg.Input(size=1, enable_events=True, key='fifth_pos')],
                [sg.Text('Inneholder bokstaver:'), 
                sg.InputText(enable_events=True, key=contains_letter_name)],
                [sg.Text('Inneholder ikke bokstaver:'), 
                sg.InputText(enable_events=True, key=not_contains_letter_name)],
                [sg.HorizontalSeparator()],
                [sg.Multiline(autoscroll=True, expand_x=True, visible=False, key='results')],
                [sg.Button('Søk', key='search'), sg.Button('Rydd', key='clear')] ]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        elif event == 'clear':
            for k,_ in values.items():
                values[k] = ''
            for name in correct_pos_names:
                window[name].update('', background_color = 'white')
            window[contains_letter_name].update('', background_color='white')
            window[not_contains_letter_name].update('', background_color='white')
            window['results'].update(visible=False)
        else:
            # Clean values
            for name in correct_pos_names:
                temp : str = values[name][:1]
                temp = temp.lower()
                if not temp.isalpha():
                    temp = ''
                window[name].update(temp)
                values[name] = temp
            
            # clean contains
            values[contains_letter_name] = clean_input_line(values[contains_letter_name])
            window[contains_letter_name].update(values[contains_letter_name])
            values[not_contains_letter_name] = clean_input_line(values[not_contains_letter_name])
            window[not_contains_letter_name].update(values[not_contains_letter_name])
            
            # Change background
            for nr,name in enumerate(correct_pos_names):
                if values[name] != '':
                    window[name].update(background_color='green')
                else:
                    window[name].update(background_color='white')
            
            if values[contains_letter_name] != '':
                window[contains_letter_name].update(background_color='yellow')
            else:
                window[contains_letter_name].update(background_color='white')
            
            if values[not_contains_letter_name] != '':
                window[not_contains_letter_name].update(background_color='yellow')
            else:
                window[not_contains_letter_name].update(background_color='white')

            # search for results
            if event == 'search':
                correct_pos : List[correct_letter] = []
                for nr, letter in enumerate(correct_pos_names):
                    if values[letter] != '':
                        correct_pos.append(create_correct_letter(nr, values[letter]))
                if check_illegal_input_values(''.join((values[name] for name in correct_pos_names)),values[contains_letter_name],values[not_contains_letter_name]):
                    results = ['Illegal input values.']
                else:
                    results = findWords(nb_dictionary, correct_pos, list(values[contains_letter_name]),list(values[not_contains_letter_name]))
                # crop results and show
                temp_results = results
                if len(temp_results) > 200:
                    temp_results = temp_results[:200]
                temp_results = ', '.join(temp_results)
                window['results'].update(temp_results,visible=True)

    window.close()

if __name__ == '__main__':
    raise SystemExit(main())