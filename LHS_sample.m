clc
clear
addpath 'E:\pipe_abaqus\20211011_NewBatch\background\algorithm\Step1_LHS'
N =5; % num of smaple
%%boundry 
colu(1,1)=5;%tube diameter
colu(1,2)=60;
colu(2,1)=1;%tube thickness
colu(2,2)=10;
colu(3,1)=20;%bending radius
colu(3,2)=225;
colu(4,1)=0.05;%fbending
colu(4,2)=0.3;
colu(5,1)=0.05;%fpressure
colu(5,2)=0.3;
colu(6,1)=0.05;%fwiper
colu(6,2)=0.3;
colu(7,1)=0;%gbending
colu(7,2)=0.25;
colu(8,1)=0;%gpressure
colu(8,2)=0.25;
colu(9,1)=0;%gwiper
colu(9,2)=0.25;
colu(10,1)=-0.25;%velocity differ between velocity of pressure die and equivalent angular velocity of bending die
colu(10,2)=0.25;
colu(11,1)=0;%initial position of pressure die
colu(11,2)=75;
colu(12,1)=0.349;%angular velocity
colu(12,2)=1.0472;
colu(13,1)=30;%bending angle
colu(13,2)=120;

%%调用函数
[X_scaled,X_normalized]=lhsdesign_modified(N,colu(:,1),colu(:,2));
% figure
% plot(X_scaled(:,1),'*')
% title('Random Variables')
% xlabel('X1')
% ylabel('X2')
% grid on
% figure
% plot(X_normalized(:,1),X_normalized(:,2),'r*')
% title('Normalized Random Variables')
% xlabel('Normalized X1')
% ylabel('Normalized X2')
% grid on

%%%%%%%%%%%%%%%delete extreme (defect) sample
xxx=[];
mm=1;
nnn=0;
YY=X_scaled;
for i=1:N
    D=YY(i,1);
    t=YY(i,2);
    bd=YY(i,3);
    agv=YY(i,12);
    difv=YY(i,10);
    
    m(i)=bd/D;%ratio between radius of bending die and diameter of tube
    n=D/t;%ratio between diameter and thickness of tube 
    nn=agv+difv;%velocity of pressure should be guranteed 
    if m(i)>2&&m(i)<5
        if n>5&&n<15
            if nn>0.1
                xxx(mm,:)=YY(i,:);
                mmm(mm)=bd/D;
                mm=mm+1;
                
            else
                nnn=nnn+1;
            end
        end
    end
end

num=size(xxx,1);
for ii=1:num
    xxx(ii,14)=(xxx(ii,13)*pi/180)/xxx(ii,12);%%%running time
end

figure(1)
plot(xxx(:,1),'*');grid on
title('original')
% figure(2)
% plot(xxx(:,2),'*');grid on
% title('picked')
size(xxx)