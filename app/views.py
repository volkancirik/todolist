from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from meccid.app.models import  Day,Task
from datetime import  datetime,timedelta
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

@login_required
def test(request):
    return render_to_response(
        'test.html', dict(), context_instance=RequestContext(request))

@login_required
def index(request):
    return render_to_response(
        'index.html', dict(), context_instance=RequestContext(request))

@login_required
def today(request):

    now = datetime.strftime(datetime.now() , "%Y/%m/%d")
    nowDate = datetime.strptime(now, "%Y/%m/%d")

    try:
        today = Day.objects.get(date = nowDate)
    except :
        today = Day.objects.create(date= nowDate)
        today.save()

    taskList = Task.objects.filter( day = today, user = request.user )
    numberOfAddedTask = taskList.count()
    i = 1
    for aTask in taskList:
        aTask.htmlID = i
        i = i+1

    return render_to_response(
        'today.html',
                {
                'taskList':taskList,
                'numberOfTasksLeft':(5-numberOfAddedTask),
                'numberOfAddedTask': numberOfAddedTask,
                }, context_instance=RequestContext(request))
@login_required
def yesterday(request):

    yester= datetime.strftime(datetime.now() - timedelta(days = 1),"%Y/%m/%d")
    yesterdayDate = datetime.strptime( yester, "%Y/%m/%d")
    taskList = []
    numberOfAddedTask = 0
    try:
        yesterday = Day.objects.get(date = yesterdayDate)
        taskList = Task.objects.filter(day = yesterday, user = request.user)
        i = 1
        for aTask in taskList:
            aTask.htmlID = i
            i = i+1

        numberOfAddedTask = taskList.count()
    except :
        pass


    return render_to_response(
            'yesterday.html',
                {
                'taskList':taskList,
                'numberOfTasksLeft':(5-numberOfAddedTask),
                'numberOfAddedTask': numberOfAddedTask,
                }, context_instance=RequestContext(request))

@login_required
def manage_task(request):

    option = request.GET.get("option")

    if option == '1':
        task_text = request.GET.get("task_text")
        givendate = request.GET.get("givendate")
        if givendate == 'none':
            givendate = datetime.strftime(datetime.now(),"%Y/%m/%d")



        theDate = datetime.strptime(givendate, "%Y/%m/%d")

        try :
            theDay = Day.objects.get(date = theDate )
        except :
            theDay = Day.objects.create(date = theDate)
        try:
            task = Task.objects.create(text = task_text, day = theDay,user = request.user )
            result = task.id
        except :
            pass


    if option == '2':
        id = request.GET.get("id")
        try:
            task = Task.objects.get(pk = int(id), user = request.user )
            task.delete()
            result = 1
        except :
            result = 0

    if option == '3':

        id = request.GET.get("task_id",None)
        tClass = request.GET.get("task_class",1)

        try:
            task = Task.objects.get( pk = int(id))
            task.taskClass = int(tClass)
            task.close_date = datetime.now()
            task.save()
            result = 1
        except :
            result = 0

    print result
    json_models = simplejson.dumps(result)
    return HttpResponse(json_models, mimetype='application/json; charset=utf8')

@login_required
def someday(request):

    somedayDate = []
    if request.method == "POST":
        somedayDate = request.POST['somedayDate']
    else:
        somedayDate = request.GET['somedayDate']

    somedayD = datetime.strptime(somedayDate, "%m/%d/%Y")
    somedayDate = datetime.strftime(somedayD,"%Y/%m/%d")

    try:
        someday = Day.objects.get(date = somedayD)
        taskList = Task.objects.filter( day = someday, user = request.user )
        numberOfAddedTask = taskList.count()
        i = 1
        for aTask in taskList:
            aTask.htmlID = i
            i = i+1

    except :
        taskList = []
        numberOfAddedTask = 0

    now = datetime.strftime(datetime.now() , "%Y/%m/%d")
    nowDate = datetime.strptime(now, "%Y/%m/%d")
    if somedayD  == nowDate:
        return redirect('/today/')
    else:
        if somedayD > nowDate:
            future = 1
        else:
            future = 0

    return render_to_response(
            'someday.html',
                {
                'taskList':taskList,
                'numberOfTasksLeft':(5-numberOfAddedTask),
                'numberOfAddedTask': numberOfAddedTask,
                'someday' : somedayDate,
                'future': future,
                }, context_instance=RequestContext(request))


@login_required
def search(request):

    keyword = []
    if request.method == "POST":
        keyword = request.POST['keyword']

        taskList = Task.objects.filter( user = request.user,text__contains = keyword )
        numberFound = taskList.count()

    if len(keyword)== 0:
            return redirect('/today/')

    return render_to_response(
        'tasksearch.html',
            {
            'taskList':taskList,
            'numberOfTasksFound':numberFound,
            'keyword': keyword
            }, context_instance=RequestContext(request))
