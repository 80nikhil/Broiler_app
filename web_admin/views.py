from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
import re
import csv
from datetime import datetime as dt 
from  .models import *
import requests
import json

class LoginView(TemplateView):  
    template_name = "login.html"
    
    def get(self, request,*args, **kwargs): 
        try:
            request.session['user_id']
            return redirect('/add-rate')
        except KeyError as e:    
            return render(request,self.template_name)
    
    def post(self, request,*args, **kwargs): 
        try:
            user_obj = user.objects.get(user_name=request.POST.get('user_name'),password=request.POST.get('password'))
            request.session['user_id'] = user_obj.id
            request.session['user_name'] = user_obj.user_name
            return redirect('/add-rate')
        except user.DoesNotExist:
            return render(request,self.template_name)

def get_special_chars(s):
    special_chars = {',',';'}
    return [char for char in s if char in special_chars]
       
class RateView(TemplateView):  
    template_name = "rate.html"
    
    def get(self, request,*args, **kwargs): 
        return render(request,self.template_name)
  
    def post(self, request,*args, **kwargs): 
        data = request.POST.get('rate')
        final_rate_dic = {}
        small_rate_dic ={}
        data_list = data.splitlines()
        if get_special_chars(data) and len(data_list) < 3:
            if len(data_list) > 1:
                data_list = data_list[-1].rsplit(get_special_chars(data)[0]) 
            else:    
                data_list = data.rsplit(get_special_chars(data)[0])   
            data_list.insert(1,data.splitlines()[0])  
            data_list[1] =  data_list[1].replace(data_list[0],'')
        new_data_list = []
        for data in data_list:
            if  re.search(r'[a-zA-Z]+', data) and re.search(r'[0-9]+', data):
                city = ''
                price = ''
                small_price = ''
                char_com = False
                cost_com = False
                data = data.replace('\xa0','').replace('.','').replace('-','')  
                for char in data:
                    if char in [' ','#']:      
                        if len(city) > 0:
                            char_com = True
                            if len(price)>0:
                                cost_com = True   
                    else:
                        try:
                            int(char)
                            if char_com and cost_com:
                                 small_price +=char
                            elif not cost_com:
                                price += char    
                        except:
                            if not char_com:
                                city += char
                            elif len(price)>0:
                                cost_com = True
                region = broiler_region.objects.filter(Q(region__iexact=city)|Q(alias_name__icontains=city)|Q(abbreviation=city)).last()
                if region:                
                    final_rate_dic[region.id] = price
                    if small_price != '': 
                        small_rate_dic[region.id] = small_price         
                else:
                    final_rate_dic[city + "(Not Available)"] = price 
                    if small_price != '':  
                        small_rate_dic[city] = small_price       
            else:
                if not re.search(r'[0-9]+', data) and data not in ['Today','Tomorrow']:
                    special_char = ['+',':','=','-','$','*','$','.','Today','Tomorrow',
                                    'with','Regards','regards','With','Chicken','Paper','Rate',
                                    'final','rate']
                    for i in special_char:
                        data = data.replace(i,'')
                    try:
                        ctype_data_obj = ctype_data.objects.filter(alias_name__icontains=data.strip()).last().id    
                        new_data_list.append(ctype_data_obj)
                    except:
                        pass       
        # ctype_data_list = ctype_data.objects.filter(alias_name__contains=new_data_list).first()
        ctype_data_list = ctype_data.objects.filter(id__in=new_data_list).first()
        final_list=[]
        for key,value in final_rate_dic.items():
            final_data={}
            try:
                int(key)
                region_obj = broiler_region.objects.get(id=key)
                key = region_obj.region
                final_data['abbreviation'] = region_obj.abbreviation
            except:
                final_data['abbreviation'] = key    
            final_data['corporate'] =  ctype_data_list.title if ctype_data_list else ""
            final_data['region'] = key
            final_data['price'] = value
            final_data['broiler'] = 'Mota' 
            final_list.append(final_data)   
        for key,value in small_rate_dic.items():
            final_data={}
            try:
                int(key)
                region_obj = broiler_region.objects.get(id=key)
                key = region_obj.region
                final_data['abbreviation'] = region_obj.abbreviation
            except:
                final_data['abbreviation'] = key  
            final_data['corporate'] =  ctype_data_list.title if ctype_data_list else ""
            final_data['region'] = key
            final_data['abbreviation'] = key
            final_data['price'] = value
            final_data['broiler'] = 'Small' 
            final_list.append(final_data)          
        context = {'final_rate_dic':final_rate_dic,'new_data_list':new_data_list,'final_data':final_list}                                       
        return render(request,self.template_name,context)

class CorporateAliasView(TemplateView):  
    template_name = "add_corporate_alias.html"
    model = ctype_data
    def get(self, request,*args, **kwargs): 
        list = self.model.objects.all().order_by('title')
        for obj in list:
            if obj.alias_name:
                obj.alias_name = ', '.join(x for x in obj.alias_name)
                obj.h_abbreviation = ','.join(broiler_region.objects.filter(ctype=obj).values_list('region',flat=True))
        context = {'list': list}
        return render(request,self.template_name,context)
  
    def post(self, request,*args, **kwargs):  
        corporate = self.model.objects.get(id=request.POST.get('corporate'))  
        if corporate.alias_name:
            new_alias = corporate.alias_name
            new_alias.append(request.POST.get('alias'))
            corporate.alias_name = new_alias
        else:
            new_alias = []
            new_alias.append(request.POST.get('alias'))
            corporate.alias_name = new_alias     
        corporate.save()                
        return redirect('/add-corporate-alias')
    
class StateAliasView(TemplateView):  
    template_name = "add_state_alias.html"
    model = state_data
    def get(self, request,*args, **kwargs): 
        list = self.model.objects.all().order_by('state')
        for obj in list:
            if obj.alias_name:
                obj.alias_name = ', '.join(x for x in obj.alias_name)
        context = {'list': list}
        return render(request,self.template_name,context)
  
    def post(self, request,*args, **kwargs):  
        state = self.model.objects.get(id=request.POST.get('state'))
        if state.alias_name:
            new_alias = state.alias_name
            new_alias.append(request.POST.get('alias'))
            state.alias_name = new_alias
        else:
            new_alias = []
            new_alias.append(request.POST.get('alias'))
            state.alias_name = new_alias     
        state.save()                   
        return redirect('/add-state-alias')   
    
class RegionAliasView(TemplateView):  
    template_name = "broiler_region_alias.html"
    model = broiler_region
    def get(self, request,*args, **kwargs): 
        list = self.model.objects.all().order_by('region')
        for obj in list:
            if obj.alias_name:
                obj.alias_name = ', '.join(x for x in obj.alias_name)
        context = {'list': list}
        return render(request,self.template_name,context)
  
    def post(self, request,*args, **kwargs):  
        state = self.model.objects.get(id=request.POST.get('state'))
        if state.alias_name:
            new_alias = state.alias_name
            new_alias.append(request.POST.get('alias'))
            state.alias_name = new_alias
        else:
            new_alias = []
            new_alias.append(request.POST.get('alias'))
            state.alias_name = new_alias     
        state.save()                   
        return redirect('/region-alias') 
    
class Get_Rate_List(APIView):
    def post(self,request,*args, **kwargs):
        response_data_list = []
        date_str = request.data['date']
        date_obj = dt.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        for obj in json.loads(request.data['data']):
            if not "Not Available" in obj['region']:
                ctype = ctype_data.objects.filter(title=obj['corporate']).last()
                region_obj = broiler_region.objects.filter(ctype=ctype,region=obj['region'],abbreviation=obj['abbreviation'])
                if region_obj.exists():
                    region_obj = region_obj.last()
                else: 
                    region_obj = broiler_region.objects.filter(alias_name__icontains=obj['region'],abbreviation=obj['abbreviation']).last()   
                if region_obj:
                    url='https://eggchi.com/uploads/images/add_rate.php'
                    payload = {
                        "regionid":int(region_obj.id),
                        "rate":float(obj['price']),
                        "pfix":'',
                        "ratetype":'broiler',
                        "createdate": formatted_date,
                        "createday": formatted_date,
                        "fixrate":0,
                        "filestamp":0,
                    }
                    # headers = { 'Content-Type': 'application/json'}
                    headers = {}
                    response_data = requests.post(url, headers=headers, data=payload,verify=False)
                    print("Request completed in {0:.0f} seconds".format(response_data.elapsed.total_seconds()))
                    if response_data.json()['status'] == True:
                        response_data_list.append(obj) 
        return Response({'message':'Record Inserted Succesfully','data':response_data},status=status.HTTP_200_OK)    
    
class Logout(TemplateView):
    def get(self,request,*args, **kwargs):
        del request.session['user_id']   
        return redirect('/')         