import json, os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Record
from .forms import RecordForm

DATA_FILE = os.path.join(settings.BASE_DIR, 'data.json')

def submit(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        save_to = request.POST.get('save_to', 'db')
        if form.is_valid():
            data = form.cleaned_data
            if save_to == 'db':
                if Record.objects.filter(name=data['name'], text=data['text']).exists():
                    messages.error(request, "Такая запись уже есть в БД!")
                else:
                    Record.objects.create(**data)
                    messages.success(request, "Сохранено в БД")
                    return redirect('/?source=db')
            else:
                records = []
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        records = json.load(f)
                records.append({'name': data['name'], 'text': data['text']})
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
                messages.success(request, "Сохранено в файл")
                return redirect('/?source=file')
    else:
        form = RecordForm()
    return render(request, 'form.html', {'form': form})

def index(request):
    source = request.GET.get('source', 'db')
    if source == 'db':
        records = Record.objects.all().order_by('-created_at')
    else:
        records = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
    return render(request, 'index.html', {'records': records, 'source': source})

def search(request):
    q = request.GET.get('q', '')
    qs = Record.objects.filter(Q(name__icontains=q) | Q(text__icontains=q))
    data = list(qs.values('id', 'name', 'text'))
    return JsonResponse({'results': data})

def edit(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Обновлено")
            return redirect('/?source=db')
    else:
        form = RecordForm(instance=record)
    return render(request, 'form.html', {'form': form, 'edit': True})

@require_POST
def delete(request, pk):
    Record.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 'ok'})