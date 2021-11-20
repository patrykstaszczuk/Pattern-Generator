from PIL import ImageDraw, Image, ImageOps, ImageFont
from schemas import SimplePolishSchema
from image import ImageBackground, Pattern


def get_width_from_user() -> int:
    while True:
        try:
            return int(input(
                'How width (in pixsels) you want the image be? Max(5616)? '))
        except ValueError:
            print('Provide a number')


def get_num_of_columns_from_user() -> int:
    while True:
        try:
            return int(input('How many letters in row you want?: '))
        except ValueError:
            print('Number required, please try again')


def get_draw_mesh_decision_from_user() -> bool:
    while True:
        try:
            return bool(int(input('Do you want to genreate background mesh?: ')))
        except ValueError:
            print('Provide a number')


def get_line_width_from_user() -> int:
    while True:
        try:
            return int(input(
                'Please input desire line width. Type 0 to use default: '))
        except ValueError:
            print('Provide a number')


def get_background_color_from_user() -> str:
    return input('Input desire background color in hex format (#c8fd92). '
                 + 'Press enter if you want to use default (white) color ')


def get_line_color_from_user() -> str:
    return input('Input desire line color in hex format (#c8fd92).'
                 + 'Press enter if you want to use default black color ')


def main() -> None:
    print('\n\n###Pattern generator###\n\n')
    print('Answer the questions below to generate pattern.')
    print('Type "1" if yes, "0" if no or provide a value if required: \n')
    while True:
        try:
            decision = int(input('1.Use default settings? '
                                 + '(width=4000px, columns=7, color=white (black lines), no mesh): '))
            break
        except ValueError:
            print('Provide a number')
    schema = SimplePolishSchema()
    if decision:
        width = 4000
        num_of_colums = 7
        background = ImageBackground(
            width=width,
            schema=schema,
            with_mesh=True,
            num_of_colums=num_of_colums).generate_image_background()
    else:
        print("Start with creating background image for your pattern....")
        width = get_width_from_user()
        num_of_colums = get_num_of_columns_from_user()
        color = get_background_color_from_user()
        with_mesh = get_draw_mesh_decision_from_user()
        background = ImageBackground(
            width=width,
            schema=schema,
            num_of_colums=num_of_colums,
            color=color,
            with_mesh=with_mesh).generate_image_background()

    text = input('Please type the text you want to draw: ')

    if decision:
        lines = Pattern(
            image=background,
            schema=schema,
            text=text)
    else:
        line_width = get_line_width_from_user()
        line_color = get_line_color_from_user()
        lines = Pattern(
            image=background,
            schema=schema,
            text=text,
            start_line_width=line_width,
            color=line_color)
    image = lines.draw()
    image.save('/Users/patrykstaszczuk/Desktop/lines.jpg', quality=100)
    print('Image is ready, you can find it inside app folder')


if __name__ == '__main__':
    main()
