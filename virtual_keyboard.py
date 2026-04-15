import cv2
import mediapipe as mp
import time


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#keys
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','BACK','DEL'],
    ['SPACE']
]

#button class
class Button:
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size

    def draw(self, img, hover=False):
        x,y = self.pos
        w,h = self.size

        color = (0,255,0) if hover else (204,136,153)
        cv2.rectangle(img, (x,y), (x+w,y+h), color, cv2.FILLED)

        # Adjust font size for longer text
        font_scale = 2 if len(self.text) > 3 else 3
        text_x = x + 10
        text_y = y + 55

        cv2.putText(img, self.text, (text_x,text_y),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, (255,255,255), 2)

    def check(self, x, y):
        return self.pos[0] < x < self.pos[0]+self.size[0] and self.pos[1] < y < self.pos[1]+self.size[1]

#buttons
buttons = []
start_x, start_y = 100,100

for i,row in enumerate(keys):
    x = start_x
    for key in row:

        # Default size
        size = [85,85]

        if key == 'SPACE':
            size = [600,85]
        elif key == 'BACK':
            size = [150,85]
        elif key == 'DEL':
            size = [120,85]

        buttons.append(Button([x, start_y + i*100], key, size))
        x += size[0] + 10

#variables
final_text = ""
hover_key = None
hover_start_time = 0
dwell_time = 0.6

cursor_visible = True
last_cursor_toggle = time.time()

#main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    index_pos = None

    #hand track
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark
        h,w,_ = img.shape

        index_pos = (int(lm[8].x*w), int(lm[8].y*h))
        cv2.circle(img, index_pos, 10, (255,0,255), cv2.FILLED)

        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    #draw keyboard
    current_hover = None
    for button in buttons:
        if index_pos and button.check(*index_pos):
            current_hover = button
            button.draw(img, hover=True)
        else:
            button.draw(img)

    # dwell click
    if current_hover:
        if hover_key != current_hover:
            hover_key = current_hover
            hover_start_time = time.time()
        else:
            if time.time() - hover_start_time > dwell_time:
                key = current_hover.text

                if key == "SPACE":
                    final_text += " "
                elif key == "BACK":
                    final_text = final_text[:-1]
                elif key == "DEL":
                    final_text = ""
                else:
                    final_text += key

                hover_key = None

    else:
        hover_key = None

    #text box
    box_x, box_y = 100, 520
    box_w, box_h = 1100, 180

    cv2.rectangle(img, (box_x, box_y), (box_x+box_w, box_y+box_h), (0,0,0), cv2.FILLED)

    #text wrap
    words = final_text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if len(test_line) < 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    visible_lines = lines[-3:]

    #draw text
    for i, line in enumerate(visible_lines):
        cv2.putText(img, line, (box_x+20, box_y+40 + i*40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)

    # cursor blink
    if time.time() - last_cursor_toggle > 0.5:
        cursor_visible = not cursor_visible
        last_cursor_toggle = time.time()

    last_line = visible_lines[-1]

    (text_width, _), _ = cv2.getTextSize(last_line, cv2.FONT_HERSHEY_PLAIN, 2, 2)

    cursor_x = box_x + 20 + text_width
    cursor_y = box_y + 40 + (len(visible_lines)-1)*40

    if cursor_visible:
        cv2.rectangle(img,
                      (cursor_x, cursor_y - 25),
                      (cursor_x + 5, cursor_y),
                      (255,255,255),
                      cv2.FILLED)

    # display
    cv2.imshow("Virtual Keyboard", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()