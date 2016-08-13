#-*- coding: UTF-8 -*-
from Acquisition import aq_inner

from Products.CMFPlone.resources import add_resource_on_request
from Products.Five.browser import BrowserView

from my315ok.products.product import Iproduct
from plone.memoize.instance import memoize
from collective.diazotheme.bootstrap.browser.homepage import HomepageView as baseview
from Products.CMFCore import permissions
from xsgs.policy.browser.interfaces import IThemeSpecific 



class FrontpageView(baseview):
     
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
        add_resource_on_request(self.request, 'xsgs-homepage')     

    
    def carouselid(self):
        return "carouselid"
    
    def active(self,i):
        if i == 0:
            return "active"
        else:
            return ""
        
    @memoize
    def carouselresult(self):
        
        out = """
        <div id="carousel-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-generic" data-slide-to="1"></li>
    <li data-target="#carousel-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>    
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-generic" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-generic" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>

</div>
        """ 
        
        braindata = self.catalog()({'object_provides':Iproduct.__identifier__, 
                                    'b_start':0,
                                    'b_size':3,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        brainnum = len(braindata)
        if brainnum == 0:return out        

        outhtml = """<div id="%s" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
        """ % (self.carouselid())
        outhtml2 = '</ol><div class="carousel-inner">'
        for i in range(brainnum):            
            out = """<li data-target='%(carouselid)s' data-slide-to='%(indexnum)s' class='%(active)s'>
            </li>""" % dict(indexnum=str(i),
                    carouselid=''.join(['#',self.carouselid()]),
                    active=self.active(i))
                                               
            outhtml = ''.join([outhtml,out])   # quick concat string
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            outimg = """<div class="%(classes)s">
                        <img src="%(imgsrc)s" alt="%(imgtitle)s"/>
                          <div class="carousel-caption">
                            <h3>%(imgtitle)s</h3>
                              </div>
                                </div>""" % dict(classes=''.join(["item ", self.active(i)]),
                     imgsrc=''.join([objurl, "/@@images/image/preview"]),imgtitle=objtitle)
            outhtml2 = ''.join([outhtml2,outimg])   # quick concat string                    
#        outhtml = outhtml +'</ol><div class="carousel-inner">'
        result = ''.join([outhtml,outhtml2])   # quick concat string
        out = """
        </div><a class="left carousel-control" href="%(carouselid)s" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="%(carouselid)s" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>""" % dict(carouselid = ''.join(["#", self.carouselid()]))
        return ''.join([result,out])
                
              
# roll zone
    @memoize
    def rollresult(self,collection=None,limit=7,words=15):
        """return roll zone html"""
        
        if collection == None:
            braindata = self.catalog()({'portal_type':'News Item',
                                    'b_start':0,
                                    'b_size':limit,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        else:

            queries = {'portal_type':'Collection','id':collection}
            ctobj = self.catalog()(queries)

            if ctobj is not None:
                # pass on batching hints to the catalog
                braindata = ctobj[0].getObject().queryCatalog(batch=True)
            else:           
                braindata = None
                      
        outhtml = """<div class="%s" data-pause="1000" data-step="1" data-speed="30" data-direction="up">
            <ul class="rolltext">
        """ % (self.rollwrapperclass())

        brainnum = len(braindata)
        if brainnum == 0 : return "roll zone"
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            fulltitle = braindata[i].Title
            if type(fulltitle) != type(""):fulltitle = fulltitle()
#             import pdb
#             pdb.set_trace()
            objtitle = self.cropTitle(fulltitle, words)
            modifydate = braindata[i].created.strftime('%Y-%m-%d')
            
            out = """<li class="rollitem">
            <span>
            <a href="%(objurl)s" title="%(fulltitle)s">%(title)s</a>
            </span>
            <span class="portletItemDetails">%(date)s</span></li>""" % dict(objurl=objurl,                                                                            
                                            title=objtitle,
                                            fulltitle = fulltitle,
                                            date= modifydate)
                                               
            outhtml = ''.join([outhtml,out])   #quick concat string
        outhtml = "%s</ul></div>" % outhtml
        return outhtml

        
    def rollheader(self):
        return u"新闻"
    
    def rollmore(self):
        return "http://www.xsgs998.com/news/"               
        
               
        
# outer html zone
    
    def outhtmlheader(self):
        return u"论坛热帖"
    
    def outhtmlmore(self):
        return "http://plone.315ok.org/"           
    
    def dataparameter(self):
        data = {
                'code':"utf-8",
                'filter':True,
                'target':"http://plone.315ok.org/",
                'tag':"div",
                'cssid':"portal_block_52_content",
                'cssclass':"dxb_bc",
                'attribute':"",
                'regexp':"",
                'index':0,   #fetch first block
                'interval':24
                }
        return data          
