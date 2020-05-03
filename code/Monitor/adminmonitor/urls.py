"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .monitormain import admin_view
from .monitormain import zookeeper_status
from .monitormain import startZookeeper
from .monitormain import stopZookeeper

from .monitormain import startKafka
from .monitormain import stopKafka
from .monitormain import kafka_status 

from .monitormain import startES
from .monitormain import stopES
from .monitormain import es_status 

from .monitormain import startWS
from .monitormain import stopWS
from .monitormain import ws_status 

from .monitormain import listener_status
from .monitormain import startListener
from .monitormain import stopListener 

from .monitormain import pushToES_status
from .monitormain import startPushToES
from .monitormain import stopPushToES

from .monitormain import analytics_status
from .monitormain import startAnalytics 
from .monitormain import stopAnalytics 

from .monitormain import last_execution_gus 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminmonitor/', admin_view),
    path('adminmonitor/zookeeperstatus', zookeeper_status),
    path('adminmonitor/startzookeeper/', startZookeeper),
    path('adminmonitor/stopzookeeper/', stopZookeeper),

    path('adminmonitor/kafkastatus', kafka_status),
    path('adminmonitor/startkafka/', startKafka),
    path('adminmonitor/stopkafka/', stopKafka),
    
    
    path('adminmonitor/esstatus', es_status),
    path('adminmonitor/startes/', startES),
    path('adminmonitor/stopes/', stopES),
    
    path('adminmonitor/wsstatus', ws_status),
    path('adminmonitor/startws/', startWS),
    path('adminmonitor/stopws/', stopWS),
    
    path('adminmonitor/listenerstatus', listener_status),
    path('adminmonitor/startlistener/', startListener),
    path('adminmonitor/stoplistener/', stopListener),

    path('adminmonitor/pushToESstatus', pushToES_status),
    path('adminmonitor/startpushToES/', startPushToES),
    path('adminmonitor/stoppushToES/', stopPushToES),  
    
    path('adminmonitor/analyticsstatus', analytics_status),
    path('adminmonitor/startanalytics/', startAnalytics),
    path('adminmonitor/stopanalytics/', stopAnalytics),
    
    path('adminmonitor/lastexecutiongus/',last_execution_gus),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
