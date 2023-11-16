from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from django.conf import settings


# Create your views here.
def upload(request):
    global column_name, data, excel_file
    if request.method == 'GET':
        return render(request, 'upload0.html')
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        fs = FileSystemStorage()
        fs.save(excel_file.name, excel_file)
        data = pd.read_excel(excel_file)
        column_name = data.iloc[0].values
        column_name_list = column_name.tolist()
        print(column_name_list)
        request.session['column_name_list'] = column_name_list
        request.session['file_name'] = excel_file.name
        return render(request, 'upload0.html')


def index(request):
    if request.method == 'GET':
        column_name_list = request.session['column_name_list']
        file_name = request.session['file_name']
        return render(request, 'index.html', {'column_name_list': column_name_list, 'file_name': file_name})


def train_model(request):
    if request.method == 'GET':
        render(request,'upload0.html')
    if request.method == 'POST':
        max_depth = int(request.POST.get('maxDepth'))
        min_samples_split = int(request.POST.get('minSamplesSplit'))
        min_samples_leaf = int(request.POST.get('minSamplesLeaf'))
        output_variable = request.POST.get('outputVariable')
        print(max_depth)
        file_name = request.session.get('file_name', None)
        if file_name is None:
            return JsonResponse({'error': 'No file name provided'})
        try:
            file_path = f'{settings.MEDIA_ROOT}/upload/{file_name}'
            dataset = pd.read_excel(file_path)
        except Exception as e:
            return JsonResponse({'error': f'Error loading dataset: {str(e)}'})

        # 分割数据集为训练集和测试集
        X = dataset.drop(columns=[output_variable])
        y = dataset[output_variable]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 创建并训练决策树模型
        clf = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split,
                                     min_samples_leaf=min_samples_leaf)
        clf.fit(X_train, y_train)

        # 在测试集上进行预测并计算准确度
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        # 返回结果
        return JsonResponse({'accuracy': accuracy})

    return HttpResponseBadRequest('Invalid request method')