import cv2
import numpy as np

def region_of_interest(img,vertices):
    mask = np.zeros_like(img)
    # channel_count = img.shape[2]
    match_mask_color = 255
    cv2.fillPoly(mask,vertices,match_mask_color)
    masked_image = cv2.bitwise_and(img,mask)
    return  masked_image

def drow_the_lines(img,lines):
    img = np.copy(img)
    # siyah görüntü oluşturulur
    blank_image = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)

    for line in lines:
        for x1,y1,x2,y2 in line:
            # siyah ekran üzerine çizgiler yerleştirilir
            cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),thickness=3)
            # print(x1,y1,x2,y2)
    # verilen görüntüleri belli bir oranla toplar birleştirir
    img = cv2.addWeighted(img,0.8,blank_image,1,0.0)
    return img


# image = cv2.imread('road.jpg')

# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
def process(image):
    # video boyutları değişkenlere atanır
    height = image.shape[0]
    width = image.shape[1]
    # videoda sadece yolun görünmesi için açılar belirlenir, üçgen oluşturulur
    region_of_interest_vertices = [
        (0,height),
        (width/1.7,height/1.7),
        (width,height)

    ]
    gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY) # alınan kareler gri'ye çevrilir
    canny_image = cv2.Canny(gray_image,100,200) #kenar çıkartma uygulanır
    # yukarıda alınan açı değerlerine göre kesme işlemi yapılır
    cropped_image = region_of_interest(canny_image,
                        np.array([region_of_interest_vertices],np.int32),)
    # cv2.imshow('cropped_image',cropped_image)
    # ulaşılamayan bazı kenarlara verilen değerler yardımıyla yaklaşılır
    lines = cv2.HoughLinesP(cropped_image,
                          rho=6,
                          theta=np.pi/60,
                          threshold=160,
                          lines=np.array([]),
                          minLineLength = 40,
                          maxLineGap = 25)
    # print('lines =',lines)
    # resim üzerine çizgiler çekilr
    image_with_lines = drow_the_lines(image,lines)
    # cv2.imshow('image_with_lines',image_with_lines)
    return image_with_lines

cap = cv2.VideoCapture('test1.mp4') # video alınır

while (cap.isOpened()): # videodan gelen görüntüler kare kare aktarılır
    ret,frame = cap.read()
    frame = process(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # q tuşuna basıldığında döngüden çıkar
        break

cap.release()
cv2.destroyAllWindows()
