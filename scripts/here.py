
# coding: utf-8

# In[6]:





# In[67]:


import herepy


# In[68]:


geocoderApi = herepy.GeocoderApi('ZScu1x4Vpek7ifBeLhbq', 'WnXYEtv1dTUluyEiXpnK4A')
response = geocoderApi.free_form('Dmitrovskoye Shosse, 9, Moscow, Russia')
routingApi = herepy.RoutingApi('ZScu1x4Vpek7ifBeLhbq', 'WnXYEtv1dTUluyEiXpnK4A')


# In[70]:


#print(response)
latitude= response.Response['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
longitude= response.Response['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']

#distance to india

routingApi = herepy.RoutingApi('ZScu1x4Vpek7ifBeLhbq', 'WnXYEtv1dTUluyEiXpnK4A')
response = routingApi.car_route([19.174, 72.86],
                                [latitude, longitude],
                                [herepy.RouteMode.car, herepy.RouteMode.fastest])
print(response)


# In[71]:


routingApi = herepy.RoutingApi('ZScu1x4Vpek7ifBeLhbq', 'WnXYEtv1dTUluyEiXpnK4A')
response = routingApi.car_route([19.174, 72.86],
                                [latitude, longitude],
                                [herepy.RouteMode.car, herepy.RouteMode.fastest])
print(response)

