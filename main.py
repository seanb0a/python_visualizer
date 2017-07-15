import pygame
import pyaudio
import wave
import sys
import audioop

CHUNK = 1024
(height, width) = (600, 800)

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
#set the pygame window title to the audio file
pygame.display.set_caption(sys.argv[1])

running = True

#pygame game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    stream.write(data)
    data = wf.readframes(CHUNK)
    #find rms (root of mean square) for the current chunk of audio data
    rms = audioop.rms(data, 2)
    print rms

    i = int(rms*0.01)

    screen.fill((255, 255, 255))
    #screen.fill((255-i, 255-i, 255-(i/2)))
    
    """
    pygame.draw.line(Surface, color, start_pos, end_pos, width)
    pygame.draw.circle(Surface, color, pos, radius, width)
    
    we can use rms to dilate the width of this line or the radius of the circle, to make it react to the audio RMS
    we can use this technique for the colour of the line/circle as well, and the screen fill if you desire
    """

    #since R,G,B must be an int, we simply cast anything which might come out as a float
    #to an integer
    pygame.draw.line(screen, (0+int(i/5), 255-i, 255-i), (400, 80), (400, 120), 1+(i*2))
    pygame.draw.circle(screen, (255-i, 255-i, 0+int(i/5)), (400, 375), 10+i, 0)
    pygame.draw.circle(screen, (0+int(i/4), 0+i, 255-i), (400, 375), 5+(i/2), 0)
    pygame.draw.circle(screen, (0+i, 255-int(i/3), 255-i), (400, 375), 1+(i/3), 0)
    #   ^  couple cool examples  ^

    pygame.draw.circle(screen, 0x000000, (700, 150+i), 20+int(i/15), 0)
    pygame.draw.circle(screen, 0x000000, (100, (height-150)-i), 20+int(i/15), 0)
    

    pygame.display.flip()
    clock.tick(3000)

stream.stop_stream()
stream.close()

p.terminate()
