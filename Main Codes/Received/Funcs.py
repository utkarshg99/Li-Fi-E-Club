import cv2 as cv
import numpy as np
import math
def ThickLine(img):
	gry=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	ta,img=cv.threshold(gry,110,255,cv.THRESH_BINARY)   #Thresholding Value can be hardcoded as there won't be much error as THE CAMERA ONLY SEES THE LINE
	kernel=cv.getStructuringElement(cv.MORPH_RECT,(17,17))   #KERNEL SIZE CAN BE CHANGED AS REQUIRED
	img=cv.morphologyEx(img,cv.MORPH_OPEN,kernel)
	img=cv.morphologyEx(img,cv.MORPH_CLOSE,kernel)     #FOR SHARPENING OF THE IMAGE OF THE LINE
	im2, con, hi= cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #CONTOURS TAKEN
	for i in range(len(con)):
		arcl=cv.arcLength(con[i],True)
		if arcl>1000:
			error_thresh=40
			contour=cv.approxPolyDP(con[i],error_thresh,True)
			n=len(contour)
		 	img=cv.drawContours(img,[contour],0,(100,100,100),5)
		 	cv.imshow(str(n),img)
		 	cv.waitKey(0)
		 	break #AS WE WILL HAVE ONLY ONE USEFUL CONTOUR, EASILY SEPARATED FROM ERRORS BY CHANGING THE THRESHOLD FOR e
def CornerPresent(contour):
	if len(contour)==4:
		return 0
	elif len(contour)==6:
		return 1
def CrossPresent(contour):
	if len(contour)==8 or len(contour)==12:
		return 1
	else:
		return 0
def CentrePoints(contour):
	if len(contour)==4:
		aa,ab=abs(contour[1][0][0]-contour[0][0][0]),abs(contour[1][0][1]-contour[0][0][1])
		ba,bb=abs(contour[2][0][0]-contour[1][0][0]),abs(contour[2][0][1]-contour[1][0][1])
		u=max(aa,ab)
		v=max(ba,bb)
		if u<v:
			p1=((contour[1][0][0]+contour[0][0][0])/2,(contour[1][0][1]+contour[0][0][1])/2)
			p2=((contour[2][0][0]+contour[3][0][0])/2,(contour[2][0][1]+contour[3][0][1])/2)
		else:
			p1=((contour[1][0][0]+contour[2][0][0])/2,(contour[1][0][1]+contour[2][0][1])/2)
			p2=((contour[0][0][0]+contour[3][0][0])/2,(contour[0][0][1]+contour[3][0][1])/2)
		return [p1,p2]
	elif len(contour)==6:
		for i in range(len(contour)):
			poly=np.delete(contour,i,0)
			if cv.pointPolygonTest(poly,(contour[i][0][0],contour[i][0][1]),False)==1:
				c1=i
				break #FOOLPROOF WAY TO DEFINE THE 6 VERTICES OF THE 'L' UNIQUELY WITH RESPECT TO EACH OTHER, STARTING FROM THE INNER CORNER VERTEX
		x=np.array([contour[c1+1],contour[c1+2]],dtype=np.int32)
		y=np.array([contour[c1-2],contour[c1-1]],dtype=np.int32)
		if abs(x[0][0][0]-x[1][0][0])>abs(x[0][0][1]-x[1][0][1]):
			horz=x
			vert=y
		else:
			horz=y
			vert=x		
		corn=np.array([contour[c1],contour[c1+3]],dtype=np.int32) #THE 6 VERTICES ARE DIVIDED INTO 3 GROUPS OF 2, DEPENDING ON POSITION ON 'L'
		hmid=((horz[0][0][0]+horz[1][0][0])/2,(horz[0][0][1]+horz[1][0][1])/2)
		vmid=((vert[0][0][0]+vert[1][0][0])/2,(vert[0][0][1]+vert[1][0][1])/2)
		cmid=((corn[0][0][0]+corn[1][0][0])/2,(corn[0][0][1]+corn[1][0][1])/2) # 'L' DEFINED BY TAKING MIDPOINTS AT THE 2 EDGES AND 1 CORNER
		return [hmid,cmid,vmid]
def ReferenceLine_and_Turn(L,THRESH=0):
	if len(L)==2:
		p1=L[0]
		p2=L[1]
		LINE=np.array([[[p1[0],p1[1]]],[[p2[0],p2[1]]]],dtype=np.int32)
		return LINE,'NO_TURN'
	elif len(L)==3:
		hmid=L[0]
		cmid=L[1]
		vmid=L[2]
		if cmid[1]<hmid[1]:
			x1,y1=hmid[0],hmid[1]
			x2,y2=cmid[0],cmid[1]
		else:
			x1,y1=cmid[0],cmid[1]
			x2,y2=hmid[0],hmid[1]
		x_top=x1+y1*(x2-x1)/y1-y2
		x_bottom=x2-(y_max-y1)*(x2-x1)/(y1-y2)
		V_LINE=np.array([[[x_top,0]],[[x_bottom,y_max]]],dtype=np.int32)
		if cmid[0]<vmid[0]:
			x1,y1=cmid[0],cmid[1]
			x2,y2=vmid[0],vmid[1]
		else:
			x1,y1=vmid[0],vmid[1]
			x2,y2=cmid[0],cmid[1]
		y_right=y1-(x_max-x1)*(y1-y2)/(x2-x1)
		y_left=y2+x2*(y1-y2)/(x2-x1)
		H_LINE=np.array([[[x_max,y_right]],[[0,y_left]]],dtype=np.int32)
		D1=cv.pointPolygonTest(H_LINE,p,True)
		D2=cv.pointPolygonTest(V_LINE,p,True) #TWO DISTANCES TAKEN, PROBLEM OF VECTORIAL DISTANCE CONTINUES
		if abs(abs(D1)-D0)<abs(abs(D2)-D0):
			CURRENT_LINE=H_LINE
			TO_BE_LINE=V_LINE
			D_CURRENT=D1
			D_TO_BE=D2
			f1=0
		else:
			CURRENT_LINE=V_LINE
			TO_BE_LINE=H_LINE
			D_CURRENT=D2
			D_TO_BE=D1
			f1=1                   # I FIND OUT WHICH LINE OF 'L' BOT WAS ON BEFORE SEEING THE CORNER, AND WHICH LINE BOT WILL BE ON AFTER TAKING THE TURN
		if ((vmid[0]<cmid[0] and hmid[1]<cmid[1]) or (vmid[0]>cmid[0] and hmid[1]>cmid[1])):
			f2=0
		else:
			f2=1
	    LINE_CHANGE_THRESHOLD=THRESH #MINIMUM SCALAR DISTANCE OF *CENTRE OF CAMERA FRAME* FROM *LINE AFTER TURN* FOR *PID LINE OF REFERENCE* TO CHANGE
		factor=f1*f2
		if factor=0:
			TURN='LEFT'
		else:
			TURN='RIGHT' #DIRECTION CONCEPTUALIZED THROUGH DIAGRAMS AND ARROWS AND COFFEE, ESPECIALLY COFFEE
		if abs(D_TO_BE)>LINE_CHANGE_THRESHOLD:
			return CURRENT_LINE,TURN
		else:
			return TO_BE_LINE,TURN
def angle_of_line(l):
	delY=(l[1][0][1]-l[0][0][1])*1.0
	delX=(l[1][0][0]-l[0][0][0])*1.0
	return math.degrees(math.atan(delY/delX))
     