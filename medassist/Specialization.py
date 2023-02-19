from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def SpecializationInterface(request):
  try:
   admin=request.session['admin']
   print("ADMIN",admin)
   return render(request,"Specialization.html",{'msg':''})
  except Exception as e:
   return render(request, "AdminLogin.html", {'msg': ''})
@xframe_options_exempt
def SpecializationDisplayAll(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        q = "select * from specialization"
        cmd.execute(q)
        records=cmd.fetchall()
        db.close()
        return render(request, "DisplayAllSpecialization.html", {'result': records})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllSpecialization.html", {'result':{}})
@xframe_options_exempt        
def SpecializationSubmit(request):
   try:
     db,cmd=Pool.ConnectionPooling()
     specialization=request.POST['specialization']
     iconfile=request.FILES['icon']
     q="insert into specialization(specialization,icon) values('{0}','{1}')".format(specialization,iconfile.name)
     cmd.execute(q)
     db.commit()
     F=open("d:/medassist/assets/"+iconfile.name,"wb")
     for chunk in iconfile.chunks():
         F.write(chunk)
     F.close()
     db.close()
     return render(request, "Specialization.html", {'msg': 'Record Submitted'})
   except Exception as e:
      return render(request, "Specialization.html", {'msg': 'Failed to Submit record'})
@xframe_options_exempt
def UpdateSpecialization(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        specialization = request.GET['specialization']
        specializationid = request.GET['specializationid']

        q = "update specialization set specialization='{0}' where specializationid={1}".format(specialization, specializationid)


        cmd.execute(q)
        db.commit()
        db.close()
        return JsonResponse({"result":True,}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)
@xframe_options_exempt
def DeleteSpecialization(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        specializationid = request.GET['specializationid']
        q = "delete from specialization  where specializationid={0}".format(specializationid)
        cmd.execute(q)
        db.commit()
        db.close()
        return JsonResponse({"result":True,}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)        
@xframe_options_exempt
def EditSpecializationPicture(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        specializationid = request.POST['specializationid']
        iconfile = request.FILES['icon']
        q = "update  specialization set icon='{0}' where specializationid={1}".format(iconfile.name,specializationid)
        cmd.execute(q)
        db.commit()
        F = open("d:/medassist/assets/" + iconfile.name, "wb")
        for chunk in iconfile.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return JsonResponse({"result":True,}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)    
@xframe_options_exempt
def SpecializationDisplayAllJSON(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        q = "select * from specialization"
        cmd.execute(q)
        records=cmd.fetchall()

        db.close()
        return JsonResponse({"result": records, }, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": {}, }, safe=False)
