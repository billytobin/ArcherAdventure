from . import vec

RESOLUTION = vec(512,512)
SCALE = 2
UPSCALED = RESOLUTION * SCALE

OFFSETS= (16,24,32,40) # offset from left, off from top, widthh of guy, height of guy

WORLD_SIZE= vec(512,512)

EPSILON = 0.01