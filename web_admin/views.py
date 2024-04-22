from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
import re
import csv
from  . models import *

def get_special_chars(s):
    special_chars = {',', ':', ';', '.'}
    return [char for char in s if char in special_chars]
       
class RateView(TemplateView):  
    template_name = "rate.html"
    
    def get(self, request,*args, **kwargs): 
        return render(request,self.template_name)
  
    def post(self, request,*args, **kwargs): 
        data = request.POST.get('rate')
        final_rate_dic = {}
        data_list = data.splitlines()
        if len(data_list) == 1:
            data_list = data.rsplit(get_special_chars(data)[0]) 
        new_data_list = []
        for data in data_list:
            if  re.search(r'[a-zA-Z]+', data) and re.search(r'[0-9]+', data):
                city = ''
                price = ''
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
                            if not cost_com:
                                price += char
                        except:
                            if not char_com:
                                city += char
                            elif len(price)>0:
                                cost_com = True
                region = broiler_region.objects.filter(region__iexact=city).last()
                if region:                
                    final_rate_dic[region.region] = price  
                else:
                    final_rate_dic[city] = price       
            else:
                if not re.search(r'[0-9]+', data) and data not in ['Today','Tomorrow','with','Regards','regards','With']:
                    special_char = ['+',':','=','-','$','*','$','.','Today','Tomorrow']
                    for i in special_char:
                        data = data.replace(i,'')
                    try:
                        ctype_data_obj = ctype_data.objects.filter(alias_name__icontains=data).last().id    
                        new_data_list.append(ctype_data_obj)
                    except:
                        pass       
        # ctype_data_list = ctype_data.objects.filter(alias_name__contains=new_data_list).first()
        ctype_data_list = ctype_data.objects.filter(id__in=new_data_list).first()
        final_list=[]
        for key,value in final_rate_dic.items():
            final_data={}
            final_data['corporate'] =  ctype_data_list.title if ctype_data_list else ""
            final_data['region'] = key
            final_data['abbreviation'] = key
            final_data['price'] = value
            final_data['broiler'] = 'Mota' 
            final_list.append(final_data)       
        context = {'final_rate_dic':final_rate_dic,'new_data_list':new_data_list,'final_data':final_list}                                       
        return render(request,self.template_name,context)

class CorporateAliasView(TemplateView):  
    template_name = "add_corporate_alias.html"
    model = ctype_data
    def get(self, request,*args, **kwargs): 
        list = self.model.objects.all().order_by('id')
        for obj in list:
            if obj.alias_name:
                obj.alias_name = ', '.join(x for x in obj.alias_name)
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
        list = self.model.objects.all().order_by('id')
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
        list = self.model.objects.all().order_by('id')
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