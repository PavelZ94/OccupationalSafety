LEXICON_COMMANDS: dict[str, str] = {
    '/mistake': 'Отправить заявку о нарушении',
    '/help': 'Узнать, что такое Near Miss'
}

start_command_text = ('Этот бот принимает заявки выявленных нарушений '
                      'требований охраны труда, промышленной и пожарной '
                      'безопасности.\n'
                      'Чтобы заявить о нарушении - отправьте команду - '
                      '/mistake\n'
                      'Чтобы вызвать справку - отправьте команду - /help')

help_command_text = ('Программа «Near-miss» — это система учета и анализа'
                     'инцидентов, которые могли бы привести к несчастным '
                     'случаям, но были предотвращены в последний момент.\n'
                     'Основной целью программы является предотвращение'
                     'будущих инцидентов путем идентификации и устранения '
                     'потенциальных опасностей.\n'
                     'Несчастные случаи на производстве могут привести к '
                     'тяжелым травмам, потере рабочей силы и, '
                     'в крайнем случае, к смерти.\n'
                     'Кроме того, они могут привести к существенным '
                     'финансовым потерям для компании в виде штрафов, '
                     'компенсаций и потери репутации.')

default_cancel_text = ('Отменять нечего.\n'
                       'Чтобы начать пользоваться ботом - '
                       'отправьте команду - /mistake')

cancel_text = ('Вы вышли из формы заполнения заявки нарушений.\n'
               'Чтобы снова перейти к заполнению заявки -'
               'отправьте команду /mistake')

enter_name_text = 'Пожалуйста, введите ваше имя'

accepted_name_text = ('Благодарю!\n\n'
                      'Теперь укажите краткую информацию о нарушении')

warning_name_text = ('То, что вы отправили, не похоже на имя\n\n'
                     'Пожалуйста, введите ваше имя\n\n'
                     'Если вы хотите прервать заполнение анкеты - '
                     'отправьте команду /cancel')

accepted_mistake_text = ('Благодарю!\n\n'
                         'Теперь укажите подробную информацию о'
                         'нарушении')

accepted_description_text = ('Благодарю!\n\n'
                             'Теперь укажите предполагаемый уровень '
                             'опасности')

accepted_level_text = 'Благодарю! Укажите помещение/место нарушения'

warning_level_text = ('Пожалуйста, пользуйтесь кнопками '
                      'при выборе уровня опасности\n\n'
                      'Если вы хотите прервать '
                      'заполнение анкеты - отправьте команду /cancel')

accepted_place_text = ('Благодарю!\n\n'
                       'Теперь загрузите фотографию нарушения')

warning_mistake_text = ('То, что вы отправили, не похоже на краткую '
                        'информацию о нарушении\n\n'
                        'Пожалуйста, введите информацию корректно\n\n'
                        'Если вы хотите прервать заполнение анкеты - '
                        'отправьте команду /cancel')

warning_description_text = ('То, что вы отправили, не похоже на подробную '
                            'информацию о нарушении\n\n'
                            'Пожалуйста, введите информацию корректно\n\n'
                            'Если вы хотите прервать заполнение анкеты - '
                            'отправьте команду /cancel')

warning_place_text = ('То, что вы отправили, не похоже на место нарушения\n\n'
                      'Пожалуйста, введите информацию корректно\n\n'
                      'Если вы хотите прервать заполнение анкеты - '
                      'отправьте команду /cancel')

warning_photo_text = ('То, что вы отправили, не похоже на фотографию '
                      'нарушения\n\n'
                      'Пожалуйста, введите информацию корректно\n\n'
                      'Если вы хотите прервать заполнение анкеты - '
                      'отправьте команду /cancel')


def accepted_request_text(id_: int) -> str:
    return (f'Благодарю! Ваша заявка зарегистрирована под номером {id_}.\n'
            f'Сотрудники Отдела охраны труда обработают его в '
            f'установленные сроки и сообщат о результатах рассмотрения')
