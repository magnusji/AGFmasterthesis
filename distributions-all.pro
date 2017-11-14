;
;
;       IDL procedure to read the analysed data of NSMR
;
;                         Masaki Tsutsumi
;
;
;   Revision on 08/December/2003
;     Both NSMR old and new formats can be read in.
;
;---------
PRO todofy, timel, year,dofy,time
;---------
;
; revised on 03/oct/2003
;
;
t0=978307200L ; 200101010000.00 UT
dofy=fix((timel-t0)/24/3600)+1          ; day of year
time=( (timel-t0) mod (3600*24L) ) /60.  ; min of day
juld=julday(1,1,2001)+dofy-1
caldat,juld,mon,day,year
dofy=julday(mon,day,year)-julday(1,1,year)+1

end
;-----------
PRO  old_nsmr_form,para_length,$
       lunr,nmet,n,err,rng,snr,pwr,az,ze,dtime,dtimee,$
       difco,difcoe,rvel,rvele,$
       year,dofy,dofy2001,time,ht
;-----------
magic='0'OL   ; Version number of ATRAD analysis suit
tstamp1=0L ; Time stamp of first data
tstamp2=0L ; Time stamp of last data
length=0L
timel=0L
offset=0L

work=intarr(para_length/4-1) & nvel=0.

;
; Met Parameter Record
;
readu, lunr, work, nvel
;print, work, nvel
nr=work(work(0)+1) ; Number of ranges

if nr gt 0 then begin

  ;
  ; Header for Met Analysed Data Record
  ;
  readu, lunr, magic, length, timel, offset
  ;print, magic, length, timel, offset

  ;
  ; Met Analysed Data Record
  ;

    ; Range,  Error, SNR, power, AOA (azimuth, zenith), decay time
    ; decay time error, diff coeff, diff coeff error, radial vel
    ; radial vel error.

  todofy, timel, year0, dofy0, tmin
  dofy01=julday(1,1,year0)+dofy0-julday(1,1,2001) ; added 20031006 TTM

  work0=0.
  er=0
  work1=fltarr(10)
  for i=0L,nr-1 do begin
    nmet=nmet+1
    readu, lunr, work0,er,work1
    ;print,'er=',er
    ;print, dofy,work0,work1
    err(nmet)=er
    rng(nmet)=work0
    snr(nmet)=work1(0)
    pwr(nmet)=work1(1)
    az(nmet)=work1(2)
    ze(nmet)=work1(3)
    dtime(nmet)=work1(4)
    dtimee(nmet)=work1(5)
    difco(nmet)=work1(6)
    difcoe(nmet)=work1(7)
    rvel(nmet)=work1(8)
    rvele(nmet)=work1(9)
    year(nmet)=year0
    dofy(nmet)=dofy0
    dofy2001(nmet)=dofy01
    time(nmet)=tmin
  endfor
endif

end
;--------------
PRO  new_nsmr_form,para_length,$
       lunr,nmet,n,err,rng,snr,pwr,esttime,az,ze,$
       dtime,dtimee,difco,difcoe,rvel,rvele,$
       year,dofy,dofy2001,time,ht
;--------------

verbose=0  ; 1:On

magic=0L   ; Version number of ATRAD analysis suit
tstamp1=0L ; Time stamp of first data
tstamp2=0L ; Time stamp of last data
length=0L
timel=0L
offset=0L


nr=0L
rfreq=0.
work1=intarr(2)
nfreq=0.
work2=lonarr(para_length/4-5)

;
; Met Parameter Record
;
readu, lunr, nr,rfreq,work1,nfreq,work2
np=work2(0) ; number of phase difference pairs
if verbose eq 1 then begin
  print, 'number of ranges=',nr
  print, 'radar frequency (MHz)=',rfreq/1000000.
  print, 'Beam dir (AZ)=',work1(0)
  print, 'Beam dir (ZE)=',work1(1)
  print, 'Nyquist vel.(m/s)=',nfreq
  print, 'number of phase difference pairs=',np
endif

if nr gt 0 then begin

  ;
  ; Header for Met Analysed Data Record
  ;
  readu, lunr, magic, length, timel, offset
  ;print, magic, length, timel, offset

  ;
  ; Met Analysed Data Record
  ;

    ; Event start time, Range,  Error, SNR, power,
    ; AOA (azimuth, zenith), decay time, decay time error,
    ; diff coeff, diff coeff error, radial vel,
    ; radial vel error, phase differences

  todofy, timel, year0, dofy0, tmin
  dofy01=julday(1,1,year0)+dofy0-julday(1,1,2001) ; added 20031006 TTM

  lengthe=length/nr  ; length of each analysed dara record

  work0=fltarr(2)
  er=0
  work1=fltarr(lengthe/4-3)

 for i=0L,nr-1 do begin
    nmet=nmet+1
    readu, lunr, work0,er,work1
    if verbose eq 1 then begin
      print, 'range=',work0(1)
      print,  'er=',er
      print, 'az,ze=',work1(2),work1(3)
    endif
    ;print, dofy,work0,work1
   ;esttime(nmet)=work0(0)
    rng(nmet)=work0(1)
    err(nmet)=er
    snr(nmet)=work1(0)
    pwr(nmet)=work1(1)
    az(nmet)=work1(2)
    ze(nmet)=work1(3)
    dtime(nmet)=work1(4)
    dtimee(nmet)=work1(5)
    difco(nmet)=work1(6)
    difcoe(nmet)=work1(7)
    rvel(nmet)=work1(8)
    rvele(nmet)=work1(9)
    year(nmet)=year0
    dofy(nmet)=dofy0
    dofy2001(nmet)=dofy01
    time(nmet)=tmin
  endfor
endif

end
;-------
PRO readmet,filer,year,dofy,dofy2001,time,rng,az,ze,ht,rvel,rvele,$
                    difco,difcoe,err,pwr,snr
;-------
;
;
;
;
;     2001/Oct/31   ht=sqrt(re^2+rng^2+2*re*rng*cos(ze))-re
;
;
;


re=6370. ; Earth's radius in km

er=0
magic=0L   ; Version number of ATRAD analysis suit
nrec=0L    ; Number of record
tstamp1=0L ; Time stamp of first data
tstamp2=0L ; Time stamp of last data

length=0L
timel=0L
offset=0L

maxnum=1000000l
err=intarr(maxnum)
year=err & dofy=err & dofy2001=err
rvel=fltarr(maxnum) & rvele=rvel & rng=rvel & dtime=rvel & dtimee=rvel
difco=rvel & difcoe=rvel & az=rvel & ze= rvel & snr=rvel & pwr=rvel
time=rvel & ht=rvel

n=-1L     ; counter
nmet=-1L  ; counter   number of meteor echoes


files=filer+'.met'
fi=0
;FOR fi=0, n_elements(files)-1 do begin

print, files

;
; Open analysed data file
;
lunr=1
close, lunr
openr, lunr, files, /xdr


;
; Information Header
;
readu,lunr,magic,nrec,tstamp1,tstamp2
todofy, tstamp1, yr,d
print,magic,nrec,tstamp1,tstamp2,' yr,day=',yr,d

while not eof(lunr) do begin
  n=n+1

  ;
  ; Header for Met Parameter Record
  ;
  readu, lunr, magic, length, timel, offset

  if length gt 0 then begin
    if magic eq '20500002'XL then begin
      new_nsmr_form,length,$
        lunr,nmet,n,err,rng,snr,pwr,esttime,az,ze,$
        dtime,dtimee,difco,difcoe,rvel,rvele,$
        year,dofy,dofy2001,time,ht
    endif else begin
      old_nsmr_form,length,$
        lunr,nmet,n,err,rng,snr,pwr,az,ze,dtime,dtimee,$
        difco,difcoe,rvel,rvele,$
        year,dofy,dofy2001,time,ht
    endelse
  endif

endwhile
close, lunr

;ENDFOR ; fi

err=err(0:nmet)
rng=rng(0:nmet)
snr=rng(0:nmet)
pwr=pwr(0:nmet)
az=az(0:nmet)
ze=ze(0:nmet)
dtime=dtime(0:nmet)
dtimee=dtimee(0:nmet)
difco=difco(0:nmet)
difcoe=difcoe(0:nmet)
rvel=rvel(0:nmet)
rvele=rvele(0:nmet)
year=year(0:nmet)
dofy=dofy(0:nmet)
dofy2001=dofy2001(0:nmet)
time=time(0:nmet)
ht=sqrt(re^2+float(rng)^2+2.*re*rng*cos(ze*!dtor))-re



print, 'nrec=',nrec
print, '# of records: ',n,' # of meteors* ',nmet

end
;-------
PRO cald, ht,difco,difer,pmax,noise,d,der,nd,pw,sn,hmin,hmax,icon
;-------
icon=0
scaleh=7 ; assumed scale height in km
nlim=3
hcenter=(hmin+hmax)/2.
d=0 & der=0 & nd=0 & pw=999 & sn=999
difer_max=100
difht_max=(hmax-hmin)/4

pos=where(difer lt difer_max,n)
if n le nlim then begin
  icon=999
  return
endif
ht=ht(pos) & difco=difco(pos) & difer=difer(pos)

; First step
factor=exp(-(ht-hcenter)/scaleh)
dlog=total(alog(difco*factor))/float(n)
d=exp(dlog)
dsq=total(alog(difco*factor)^2)/float(n)
dstlog=sqrt(dsq-dlog^2)
der=exp(dstlog/sqrt(n))-1.
;der=d*der
nd=n
pw=total(pmax)/n
sn=total(noise)/n
htmn=total(ht)/n
difht=(hmax+hmin)/2.-htmn
if abs(difht) ge difht_max then begin
  icon=999
  return
endif

nused=n

; Second step
omitfactor=1.65
pos=where(abs(alog(difco)-dlog) lt dstlog*omitfactor,n)
if n ge nlim then begin
  ht2=ht(pos) & difco2=difco(pos) & difer2=difer(pos)
  factor=exp(-(ht2-hcenter)/scaleh)
  dlog2=total(alog(difco2*factor))/float(n)
  dsq2=total(alog(difco2*factor)^2)/float(n)
  dstlog2=sqrt(dsq2-dlog2^2)
  if dstlog2 lt dstlog then begin
    ;print,'D d d der der: ',d,exp(dlog2),der,exp(dstlog2/sqrt(n))
    d=exp(dlog2)
    der=exp(dstlog2/sqrt(n))-1. ; *100=%
    ;der=d*der
    nd=n
    pw=total(pmax(pos))/n
    noise=total(noise(pos))/n
    htmn=total(ht)/n
    difht=(hmax+hmin)/2.-htmn
    if abs(difht) ge difht_max then begin
      icon=999
      return
    endif
  endif
endif

end
;-----------
PRO calhwind, az,ze,time,ht,rdw,pmax,noise,dofy_st,dofy,nmean,$
        hmin,hmax,tmin,tmax,u,v,ere,ern,ste,stn,nused,pw,sn,icon,difsq
;-----------
;
;
;  time: hr (float)
;
;
;
icon=0
nlim=3
u=999 & v=999 & ere=999 & ern=999 & ste=999 & stn=999 & pw=999 & sn=999
difht_max=(hmax-hmin)/4

n=n_elements(az)
if n lt nlim then begin
  icon=999
  return
endif

rw=rdw ;   For NSMR 04/may/2001
       ;

w_d=nmean/2-abs(dofy-dofy_st-nmean/2)+1
        ; maximum weight at the center of nmean days

; First step
w=fltarr(n)+1 ; weight
deltat=(time-tmin)/(tmax-tmin)*2.-1.
deltah=(ht-hmin)/(hmax-hmin)*2.-1.
w=1./(deltat^2+deltah^2+1.) * w_d
w=1./(deltat^2+deltah^2+.1) * w_d
;print, w
c=cos(az*!pi/180.)*sin(ze*!pi/180.)
s=sin(az*!pi/180.)*sin(ze*!pi/180.)
ss=total(s*s*w)  & cc=total(c*c*w)
sc=total(s*c*w)  & rs=total(rw*s*w)
rc=total(rw*c*w) & rr=total(rw*rw*w)
sumw=total(w)    & delta=ss*cc-sc*sc
;if sc ne 0. then begin  ; ?????
if delta ne 0. then begin
  u=(cc*rs-sc*rc)/delta
  v=(ss*rc-sc*rs)/delta
;   estimate observation error of radial wind vel.
  raderr=(v*v*cc+u*u*ss+rr+2.*(v*u*sc-v*rc-u*rs))/sumw
;   The number of independent vel. is n/2.
  ere=cc*raderr/delta & ste=sqrt(ere) & ere=sqrt(ere/n*2.)
  ern=ss*raderr/delta & stn=sqrt(ern) & ern=sqrt(ern/n*2.)
  pw=total(pmax*w)/total(w)
  sn=total(noise*w)/total(w)
  htmn=total(ht*w)/total(w)
endif else begin
  return
endelse

difht=(hmax+hmin)/2.-htmn
if abs(difht) ge difht_max then begin
  icon=999
  return
endif

difsq=abs(rw-s*u-c*v)

nused=n

; Second step
factor=1.65 ; 10% of data
if ste gt 20 or stn gt 20 then begin
  nice=where(difsq lt sqrt(raderr)*factor,nn)
 ;nice=where(difsq lt sqrt(raderr)*factor and difsq le 50,nn)
 ;nice=where(difsq le 50,nn)
  if nn ge nlim then begin
    w=fltarr(nn)+1 ; weight
    deltat=(time(nice)-tmin)/(tmax-tmin)*2-1.
    deltah=(ht(nice)-hmin)/(hmax-hmin)*2-1.
    w=1./(deltat^2+deltah^2+1.)
    c=cos(az(nice)*!pi/180.)*sin(ze(nice)*!pi/180.)
    s=sin(az(nice)*!pi/180.)*sin(ze(nice)*!pi/180.)
    ss=total(s*s*w)  & cc=total(c*c*w)
    sc=total(s*c*w)  & rs=total(rw(nice)*s*w)
    rc=total(rw(nice)*c*w) & rr=total(rw(nice)*rw(nice)*w)
    sumw=total(w)    & delta=ss*cc-sc*sc
   ;if sc ne 0. then begin ; ?????
    if delta ne 0. then begin
      u2=(cc*rs-sc*rc)/delta
      v2=(ss*rc-sc*rs)/delta
;       estimate observation error of radial wind vel.
      raderr=(v*v*cc+u*u*ss+rr+2.*(v*u*sc-v*rc-u*rs))/sumw
      ere2=cc*raderr/delta & ste2=sqrt(ere2) & ere2=sqrt(ere2/nn*2.)
      ern2=ss*raderr/delta & stn2=sqrt(ern2) & ern2=sqrt(ern2/nn*2.)
      if ste2 lt ste and stn2 lt stn then begin
        ;print, 'Fisrt ,Second: ',n,nn,fix(ere),fix(ere2),fix(ste),fix(ste2)
        u=u2 & v=v2 & ere=ere2 & ern=ern2 & ste=ste2 & stn=stn2
        pw=total(pmax(nice)*w)/total(w)
        sn=total(noise(nice)*w)/total(w)
        nused=nn
        difsq=abs(rw(nice)-s*u-c*v)
        htmn=total(ht*w)/total(w)
      endif
    endif
  endif
endif

difht=(hmax+hmin)/2.-htmn
if abs(difht) ge difht_max then begin
  icon=999
endif

end
;------------
PRO  writeout,dofy2001,t,ht,u,v,ere,ern,nw,d,der,nd,lunw
;------------
hr=fix(t)
mm=fix( (t mod 1)*60)
juld=julday(1,1,2001)-1+dofy2001
caldat,juld,mon,day,year
dofy=julday(mon,day,year)-julday(1,1,year)+1

if abs(u) lt 300 and abs(v) lt 300 and ere lt 99 and ern lt 99 and nw ge 2 then $
  printf,lunw,format='(i4,i3,2i2,x,i3,i4,i4,i3,i3,i3,i4,i4,i3)',$
         year,dofy,hr,mm,ht,u,v,ere,ern,nw<999, $
         fix(d*10<9999),fix(der*100<999),nd<999
end
;-----------
PRO caldwind,uwork,vwork,eruwork,ervwork,nwwork,dwork,derwork,ndwork,$
             yr,day,ht,unit
;-----------
nt=(size(uwork))(1)
nlim=nt/2
nht=(size(uwork))(2)
for i=0,nht-1 do begin
  pos=where(uwork(*,i) lt 999 and nwwork(*,i) ge 5 and $
            eruwork(*,i) lt 50 and ervwork(*,i) lt 50,c)
  if c ge nlim then begin
    ud=total(uwork(pos,i))/float(c)
    vd=total(vwork(pos,i))/float(c)
    eru=sqrt(total(float(uwork(pos,i))^2)/float(c)-ud^2)/sqrt(c)
    erv=sqrt(total(float(vwork(pos,i))^2)/float(c)-vd^2)/sqrt(c)

    dd=999
    der=999
    c2=0
    pos2=where(dwork(*,i) lt 999 and ndwork(*,i) ge 5,c2)
    if c2 ge nlim then begin
     dd=total(dwork(pos2,i))/float(c2)
     der=sqrt(total(float(dwork(pos2,i)^2))/float(c2)-dd^2)/sqrt(c2)
    endif

    printf,unit,format='(i2,i3,i3,2i4,2i3,f5.1,f4.1,i3,x,a,2i4,i3)',$
      yr mod 100,day,ht(i),fix(ud),fix(vd),fix(eru),fix(erv),0.,0.,c,'o',fix(dd*10<999),fix(der*10<999),c2<999
  endif
endfor

end
;----------
; MAIN
;----------
device,decomposed=0
;
;
;   Wind at X (UT: hr) is estimated using meteor echoes detected
;   between X and X+treso (hr).
;
;
;
;
;
close,19
openw,19,'g:\projects\nsmr\distribution_ht.txt'
treso=2 ; hr
nlim=3  ; min. number of echoes in each bin

tstep=1  ; hr
minh=66. ; km
maxh=110.; km
hstep=1. ; km               ; CHRIS MOD - 2x oversampling
nht=fix((maxh-minh)/hstep)
difsq=intarr(100)

rwmax=100      ; m/s
rwemax=5       ; m/s
zemin=10       ; degree
zemax=90       ; degree
pkdifmax=5     ; second
minthetamax=20 ;

scaleh=7       ; model scale height km
const=10.^(-6) ; a constant

uwork=intarr(24,nht)  ; working area
vwork=uwork           ;
eruwork=uwork         ;
ervwork=uwork         ;
nwwork=uwork          ;
dwork=uwork       ;
derwork=uwork         ;
ndwork=uwork          ;



;
; Open output file
;
lunw=20
;print, 'Enter ouput file name'
;fout=' '
;read,fout
;close,lunw
;openw,lunw,fout

;lunwd=15
;close,lunwd
;openw,lunwd,fout+'.d'

;
; height resolution
;
;print, 'Select height resolution  0:2km 1:4km 2:8km'
;read,hreso
hreso=0
hreso=2^(hreso+1)
ht2=fix(minh+indgen(nht)*hstep+hreso/2)
;
; time resolution
;
;print, 'Select time resolution  0:1hr 1:2hr 2:4hr 3:8hr'
;read,treso
treso=0
treso=2^treso
if treso eq 1 then tstep=0.5 else tstep =1

;print, '0:normal 1:3day 2:5day mean 3:10day mean 4:30day mean'
;read, meanday
meanday=0
if meanday eq 1 then begin
  nmean=3
  step=1
endif else if meanday eq 2 then begin
  nmean=5
  step=1
endif else if meanday eq 3 then begin
  nmean=10
  step=2
endif else if meanday eq 4 then begin
  nmean=30
  step=5
endif else begin ; normal
  meanday=0
  step=1
  nmean=2   ; not 1
endelse

;
; Read data
;
;print, 'Enter file name'
;file=' '
;read,file
;file=dialog_pickfile(path='r:\NSMR\',filter='*.met')
filenames=findfile('r:\meteor\NSMR\*.met',count=nfiles)
;filesdone=findfile('c:\projects\nsmr\dataB\*.txt',count=dfiles)

;if dfiles EQ 0 then dfiles=1 ; in case there *were* no files from before!
for ifile=0,nfiles-1 do begin    ;%%%%%%%%%%%%%%%%%%%%file read loop%%%%%%%%%%%%%%%%%%
file=filenames(ifile)
fout='g:\projects\nsmr\temp_met_data.txt'
close,lunw
openw,lunw,fout

readmet,strmid(file,0,strlen(file)-4),year,dofy,dofy2001,time,range,az,ze,ht,rw,rwe,$
                    difco,difer,dcon,pwr,snr

;--------------------------------Chris plot distributions bit------------------------

nm=size(az,/n_elements)
el=90.0-ze
n=intarr(201)
h=findgen(201)
for iz=0,199 do begin
  result=where(ht gt iz and ht le iz+1 and dcon eq 0,nn)
  if nn ge 0 then n(iz)=nn
endfor
igood=where(dcon eq 0, ngood)
ibad=where(dcon ne 0)
ght=ht(igood) & bht=ht(ibad)
gaz=az(igood) & baz=az(ibad)
gze=ze(igood) & bze=ze(ibad)

nmet=fix(total(n(70:110)))
significants=where(snr ge 130,nmet)

device,decomposed=0
goto,skipazimuth

loadct,15
usersym,cos(!pi/18.*findgen(36)),sin(!pi/18.*findgen(36)),/fill
!p.multi=[0,2,1]
window,0,xsize=1200,ysize=600
plot,/POLAR,/iso,ze,!pi*(450-az)/180.0,psym=8,color=0,background=255,$
    xrange=[-100,100],/xstyle,yrange=[-100,100],/ystyle,$
    xtitle='west-east (deg)',ytitle='south-north (deg)',$
    title='off zenith angles',charsize=1.5,xmargin=[8,8],ymargin=[5,5]
oplot,/POLAR,gze,!pi*(450-gaz)/180.0,psym=8,color=127
oplot,/POLAR,bze,!pi*(450-baz)/180.0,psym=8,color=17

oplot,/polar,replicate(90,360),!pi/180.0*findgen(360),linestyle=2,color=25
;
skipazimuth:
window,1
plot,n,h,color=0,background=255,xtitle='# meteors',ytitle='height (km)',$
     charsize=1.5,xmargin=[5,3],ymargin=[5,5],yrange=[70,110],$
     title='Total '+strtrim(nmet,2)+' meteors on '+strmid(file,strlen(file)-16,8)
oplot,n,h,color=127
;xyouts,100,72,'Total '+strmid(nmet,2)+' meteors on '+strmid(file,strlen(file)-16,8),color=0,charsize=2
;write_png,'s:\ftproot\nsmr-ana\distribution-'+strmid(file,strlen(file)-16,8)+'.png',tvrd(true=1)
!p.multi=0
;
printf,19,strmid(file,strlen(file)-16,8),n(70:100)
;___________________________________________________________________________________

; Estimate horizontal wind vel.
;

;for day=min(dofy),max(dofy),step do begin
for day=min(dofy2001),max(dofy2001),step do begin   ; 20031006 TTM
  print, 'Day of year: ',day

  pos0=where(dofy2001 ge day and dofy2001 lt (day+nmean),c)
  if c lt 1 then goto,nextday
  pos1=where(dcon(pos0) eq 0 and $
             ze(pos0) ge zemin and ze(pos0) lt zemax and $
             rwe(pos0) lt rwemax and $
             abs(rw(pos0)) lt rwmax and $
             difco(pos0) ge const*exp(ht(pos0)/scaleh), c)

  if c ge nlim then begin
    dcon1=dcon(pos0(pos1))
    dofy1=dofy2001(pos0(pos1))
    time1=time(pos0(pos1)) ; min
    az1=az(pos0(pos1))
    ze1=ze(pos0(pos1))
    ht1=ht(pos0(pos1))
    rw1=rw(pos0(pos1))
    rwe1=rwe(pos0(pos1))
    difco1=difco(pos0(pos1))
    difer1=difer(pos0(pos1))
    dcon1=dcon(pos0(pos1))
    pwr1=pwr(pos0(pos1))
    snr1=snr(pos0(pos1))

    nwwork(*)=0
    if meanday eq 0 then day2001_2=day else day2001_2=day+nmean/2

    hr=time1/60.+(dofy1-1)*24.

    for t=0.,23.5,tstep do begin
    for h=0,nht-1 do begin
      hi=minh+h*hstep

     ;
     ; Wind Vel.
     ;

       if meanday eq 0 then begin ; no superposition
         pos=where( $
           hr ge (day*24L-24+t) and $              ; time (hr long int.)
           hr lt (day*24L-24+t+treso) and $
           ht1 ge hi and ht1 lt (hi+hreso), n)    ; ht
       endif else begin
         if t+treso gt 24. then begin
           pos=where($
             ( hr mod 24 ge t or hr mod 24 lt (t+treso) mod 24 ) and $
             ht1 ge hi and ht1 lt (hi+hreso), n)
         endif else begin
           pos=where((hr mod 24) ge t and (hr mod 24) lt t+treso and $
                      ht1 ge hi and ht1 lt (hi+hreso), n)
         endelse
       endelse

       u=999 & v=999 & ere=999 & ern=999 & nw=0 & ste=999 & stn=999
       if n ge nlim then begin
         calhwind, az1(pos),ze1(pos),time1(pos)/60.,ht1(pos),rw1(pos),$
             pwr1(pos),snr1(pos),day,dofy1(pos),nmean,$
             hi,hi+hreso,t,t+treso,u,v,ere,ern,ste,stn,nw,pw,sn,icon,difsq0
         if icon eq 0 then  $
           difsq=difsq+histogram(difsq0,min=0,max=99)


       endif

       uwork(t,h)=u & vwork(t,h)=v & nwwork(t,h)=nw
       eruwork(t,h)=ere & ervwork(t,h)=ern

     ;
     ; Diffusion coefficient
     ;
       scaleh=7 ; model scale H
       const=10.^(-6)
       if meanday eq 0 then begin
         pos=where(dcon1 eq 0 and $
           hr ge (day*24L-24+t) and hr lt (day*24L-24+t+treso) and $
           ht1 ge hi and ht1 lt (hi+hreso),n)
       endif else begin
         if t+treso gt 24. then begin
           pos=where(dcon1 eq 0 and $
             ( hr mod 24 ge t or hr mod 24 lt (t+treso) mod 24 ) and $
             ht1 ge hi and ht1 lt (hi+hreso), n)
         endif else begin
           pos=where(dcon1 eq 0 and $
                     (hr mod 24) ge t and (hr mod 24) lt t+treso and $
                      ht1 ge hi and ht1 lt (hi+hreso), n)
         endelse
       endelse

       d=0 & der=0 & nd=0
       if n ge nlim then begin
         cald,ht1(pos),difco1(pos),difer1(pos),pwr1(pos),snr1(pos),$
              d,der,nd,pwd,snd,hi,hi+hreso,icon
         if icon eq 0 then $
           dwork(t,h)=d & derwork(t,h)=der & ndwork(t,h)=nd
       endif


     ;
     ; Write out
     ;
       writeout,day2001_2,t,hi+hreso/2, $
                u,v,ste,stn,nw,d,der,nd,lunw

    endfor
    endfor

    ; Daily mean wind and D
   ;caldwind,uwork,vwork,eruwork,ervwork,nwwork,dwork,derwork,ndwork,$
   ;         year,day2,ht2,lunwd

  endif
  nextday:
endfor ; day

close, lunw
;close, lunwd
endfor
close,19
end
