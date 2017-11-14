; reads distribution_ht.txt and looks for time evolution
;
device,decomposed=0

n=file_lines('g:\projects\nsmr\distribution_ht.txt')/4  ;4 lines per record - output from distribution_all.pro
close,1
openr,1,'g:\projects\nsmr\distribution_ht.txt'
y=intarr(n)
m=intarr(n)
d=intarr(n)
e=intarr(n,31)
ct=strarr(n)

buffer=lonarr(32,n)
readf,1,buffer
close,1

y(*)=buffer(0,*)/10000
m(*)=(buffer(0,*) mod 1000)/100
d(*)=(buffer(0,*) mod 1000) mod 100
e(*,*)=rotate(buffer(1:31,*),4)

ct(*)=string(buffer(0,*))
y(*)=fix(strmid(ct(*),4,4))
m(*)=fix(strmid(ct(*),8,2))
d(*)=fix(strmid(ct(*),10,2))

t=julday(m,d,y)

dummy=label_date(date_format=['%Y'])
loadct,39
xr=[julday(3,1,2001),julday(3,1,2014)]
nl=19
cl=[indgen(nl)*50,9999]
cc=fix(indgen(nl+1)*255.0/(nl+1))
ca=strtrim(cl,2) & ca(0)=' ' & ca(nl)='>1000'
window,0,xsize=1000,ysize=400
contour,e,t,indgen(31)+70,color=0,background=255,xtickformat='label_date',xtickunits=['Time'],xrange=xr,/xstyle,$
       yrange=[70,100],/ystyle,ytitle="altitude (km), 78!Uo!NN",charsize=1.5,levels=cl,/cell_fill,xmargin=[8,10]
make_key,colors=cc,labels=ca,title="detections per day",orientation=1,charsize=1
write_png,'g:\projects\nsmr\2014\meteor_detections.png',tvrd(/true)

ga=fltarr(n)
gw=fltarr(n)
gp=fltarr(n)
for i=0,n-1 do begin
  vect=fltarr(31)
  vect(*)=e(i:i,*)
  res=gaussfit(indgen(31)+70,vect,coeffs,nterms=3,chisq=chisq)
  if coeffs(2) le 2 or coeffs(2) ge 8 then coeffs(*)=!values.f_nan
  if total(vect) le 600 then coeffs(*)=!values.f_nan  ; less than 25 echoes per hour
  ga(i)=coeffs(0)
  gw(i)=coeffs(2)
  gp(i)=coeffs(1)
endfor         

ok=where(gp ge 70)
xx=t(ok)-xr(0)
yy=gp(ok)
yy=smooth(gp(ok),30)
cc=ladfit(xx,yy)
ce=lsqfit_error(xx,yy,cc)
ccc=string(cc(1)*3652.5,format='(f4.2)')
cce=string(ce(1)*3652.5,format='(f4.2)')

ok2005=where(t(ok) ge julday(5,1,2005))
xxx=xx(ok2005)
yyy=yy(ok2005)
cc2005=ladfit(xxx,yyy)
ce2005=lsqfit_error(xxx,yyy,cc2005)
ccc2005=string(cc2005(1)*3652.5,format='(f4.2)')
cce2005=string(ce2005(1)*3652.5,format='(f4.2)')
xr2005=[julday(5,1,2005),julday(3,1,2010)]

window,1,xsize=1000,ysize=400
plot,t(ok),smooth(gp(ok),30),color=0,background=255,xtickformat='label_date',xtickunits=['Time'],xrange=xr,/xstyle,$
       yrange=[85,95],/ystyle,ytitle="altitude of max echo density (km), 78!Uo!NN",charsize=1.5,xmargin=[8,10]
oplot,xr,cc(0)-cc(1)*xr(0)+cc(1)*xr,color=250
oplot,xr2005,cc2005(0)-cc2005(1)*xr(0)+cc2005(1)*xr2005,color=210
oplot,[julday(10,1,2001),julday(10,1,2001)],[0,100],color=50 & xyouts,julday(10,1,2001),85.5,' 4-bit -->',color=50
oplot,[julday( 5,1,2005),julday( 5,1,2005)],[0,100],color=50 & xyouts,julday(05,1,2005),85.5,' balun -->',color=50
xyouts,julday(6,1,2005),94,'overall trend= '+ccc+' +/- '+cce+' kmdecade!U-1!N',color=250
xyouts,julday(6,1,2005),93,'trend (2005-)= '+ccc2005+' +/- '+cce2005+' kmdecade!U-1!N',color=210
write_png,'g:\projects\nsmr\2014\meteor_height.png',tvrd(/true)

window,2,xsize=1000,ysize=400
plot,t,gw,color=0,background=255,xtickformat='label_date',xtickunits=['Time'],xrange=xr,/xstyle,$
       ytitle="width of echo density (km), 78!Uo!NN",charsize=1.5,xmargin=[8,10]
oplot,[julday(10,1,2001),julday(10,1,2001)],[0,100],color=50 & xyouts,julday(10,1,2001),0.5,' 4-bit -->',color=50
oplot,[julday( 5,1,2005),julday( 5,1,2005)],[0,100],color=50 & xyouts,julday(05,1,2005),0.5,' balun -->',color=50
write_png,'g:\projects\nsmr\2014\meteor_width.png',tvrd(/true)

end
