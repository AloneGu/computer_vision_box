import cv2
img = cv2.imread('../data/orgimg_102.jpg')

view_config = {
    '0': {'LOI_LEFT': (280, 210),
          'LOI_RIGHT': (420, 210),
          'ROI_X_MIN': 200,
          'ROI_X_MAX': 450,
          'ROI_Y_MIN': 80,
          'ROI_Y_MAX': 300,
          'ORIENTATION':'UPDOWN',
          'DIRECTION':'DOWN'
          },
    '1': {'LOI_LEFT': (175, 0),
          'LOI_RIGHT': (175, 120),
          'ROI_X_MIN': 100,
          'ROI_X_MAX': 250,
          'ROI_Y_MIN': 0,
          'ROI_Y_MAX': 120,
          'ORIENTATION':'LEFTRIGHT',
          'DIRECTION':'LEFT'}
}

for v in view_config:
    x,y,x2,y2 = view_config[v]['ROI_X_MIN'],view_config[v]['ROI_Y_MIN'],view_config[v]['ROI_X_MAX'],view_config[v]['ROI_Y_MAX']
    cv2.rectangle(img,(x,y),(x2,y2),(0,0,255),thickness=3)
    cv2.line(img,view_config[v]['LOI_LEFT'],view_config[v]['LOI_RIGHT'],(0,255,0),thickness=3)
cv2.imshow('t',img)
cv2.waitKey(0)
cv2.destroyAllWindows()