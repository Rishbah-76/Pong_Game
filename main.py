from time import sleep
import pygame 

pygame.init()
WIDTH, HEIGHT =700,500
WIN= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Settinhg FPS
FPS=60

# Defining Color Variables
BLACK=(0,0,0)
WHITE=(255,255,255)
TURQUOISE=(175,238,238)
PINK_ORANGE=(248, 152, 128)
SADDLE_BROWN=(139,69,19)

# Defining Ball Variables
MAX_VEL=6
BALL_RADIUS=7

# Defining font Variables
SCORE_FONT=pygame.font.SysFont("comicsans",50)
WINING_SCORE=10

#Setting class for Paddles
PADDLE_WIDTH,PADDLE_HEIGHT=20,100
class Paddle:
    COLOR1,COLOR2=WHITE,TURQUOISE
    VEL=4
    def __init__(self,x,y,width,height):
        self.x = self.orignal_x = x
        self.y = self.orignal_y = y
        self.width = width
        self.height = height

    def draw_paddle(self,win):
        pygame.draw.rect(win,self.COLOR2,(self.x,self.y,self.width,self.height))

    def paddle_movement(self,up=True):
        if up == True:
            self.y=self.y-self.VEL
        else:
            self.y=self.y+self.VEL
    def reset_paddle(self):
        self.x=self.orignal_x
        self.y=self.orignal_y


#defining for handle collision
def handle_collision(ball,left_paddle,right_paddle):
    # For ceiling colision
    if ball.y+  ball.radius>=HEIGHT:
        ball.y_vel*=-1
    elif ball.y - ball.radius<=0:
        ball.y_vel*=-1

    #now for left_paddle and ball collision
    if ball.x_vel<0:
        if ball.y>=left_paddle.y and ball.y<=left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel*=-1

                #For ball_y_velocity on right_paddle
                middle_y=left_paddle.y+ left_paddle.height//2
                difference_in_y=middle_y-ball.y
                reduction_factor= (left_paddle.height/2)/ball.MAX_VEL
                y_vel=difference_in_y/reduction_factor
                ball.y_vel=-1*y_vel
                
    #For right_paddle and ball collision
    else:
        if ball.y>=right_paddle.y and ball.y<=(right_paddle.y + right_paddle.height):
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel*=-1
                #For ball_y_velocity on right_paddle
                middle_y=left_paddle.y+ left_paddle.height//2
                difference_in_y=middle_y-ball.y
                reduction_factor= (left_paddle.height/2)/ball.MAX_VEL
                y_vel=difference_in_y/reduction_factor
                ball.y_vel=-1*y_vel
                
                
# Making class for Ball 
class Ball:
    MAX_VEL=6
    COLOR=WHITE
    def __init__(self,x,y,radius):
        self.x =self.orignal_x = x
        self.y = self.orignal_y = y
        self.radius = radius
        self.x_vel=MAX_VEL
        self.y_vel=0

    def draw_ball(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)

    def move_ball(self):
        self.x=self.x+self.x_vel
        self.y=self.y+self.y_vel
    def reset_ball(self):
        self.x=self.orignal_x
        self.y=self.orignal_y

# Defining the person to show on Windows Finally
def draw(win,paddles,ball,left_score,right_score):
    win.fill(BLACK)
    #Adding score

    #These two lines will give us a drawable object
    left_score_text=SCORE_FONT.render(f"{left_score}",1,PINK_ORANGE)
    right_score_text=SCORE_FONT.render(f"{right_score}",1,PINK_ORANGE)
    #Applying the text object
    win.blit(left_score_text,(WIDTH//4-left_score_text.get_width(),20))
    win.blit(right_score_text,(3*WIDTH//4-right_score_text.get_width(),20))

    for paddle in paddles:
        paddle.draw_paddle(win)
    
    # Adding Dash line
    for i in range(10,HEIGHT,HEIGHT//20):
        if i % 2==1:
            continue
        pygame.draw.rect(win,PINK_ORANGE,(WIDTH//2-5,i,5,HEIGHT//20))

    #Adding ball
    ball.draw_ball(win)

    pygame.display.update() #just like stateful widget

#defining handle_movement depending on the Keys
def handle_paddle_movement(keys,left_paddle, right_paddle):
    if keys[pygame.K_w] and (left_paddle.y - left_paddle.VEL>=0) :
        left_paddle.paddle_movement(up=True)
    if keys[pygame.K_s] and (left_paddle.y + left_paddle.VEL + left_paddle.height <=HEIGHT):
        left_paddle.paddle_movement(up=False)
    if keys[pygame.K_UP] and (right_paddle.y - right_paddle.VEL>=0):
        right_paddle.paddle_movement(up=True)
    if keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.VEL + right_paddle.height <=HEIGHT):
        right_paddle.paddle_movement(up=False)


def main():
    run= True
    clock=pygame.time.Clock()
    left_paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle=Paddle(WIDTH-10-PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)

    #Getting Ball
    ball=Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS)

    #Setting score
    left_score=0
    right_score=0

    while run:
        # Maintaining constant FPS
        clock.tick(FPS)

        # Drwaing the ball, paddles and score
        draw(WIN,[left_paddle,right_paddle],ball,left_score,right_score)
        for event in pygame.event.get(): #getting the events
            if event.type == pygame.QUIT:
                run= False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run= False
                    break
            
        #Storing the keys to handle paddle movement
        keys =pygame.key.get_pressed()

        #MAking the ball move intially in x direction
        ball.move_ball()
        
        #Handling Paddle Movement
        handle_paddle_movement(keys,left_paddle, right_paddle)
        
        #Handling colision 
        handle_collision(ball,left_paddle,right_paddle)

        #Adjusting score
        if ball.x<0:
            right_score+=1
            #Reseting the ball and paddle
            ball.reset_ball()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()
            sleep(1/2-0.09)
            ball.x_vel*=-1

        elif ball.x> WIDTH:
            left_score+=1
            #Reseting the ball and paddle
            ball.reset_ball()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()
            sleep(1/2-0.09)
            ball.x_vel*=-1
        
        #Checking if anyone WON
        won=False
        if left_score>=WINING_SCORE:
            won=True
            win_text="Left Player Won!!"
        elif right_score>=WINING_SCORE:
            won=True
            win_text="Right Player Won!!"

        if won:
            text=SCORE_FONT.render(f"{win_text}",1,SADDLE_BROWN)
            WIN.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-text.get_height()//2))
            pygame.display.update()
            sleep(3)
            ball.reset_ball()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()
            left_score=0
            right_score=0

    pygame.quit()

if __name__ == "__main__":
    main()