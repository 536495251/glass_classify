import json

import joblib
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
        return render(request, 'upload.html')
    if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        fs = FileSystemStorage()
        fs.save(excel_file.name, excel_file)
        data = pd.read_excel(excel_file)
        column_names_list = data.columns.tolist()
        print(column_names_list)
        request.session['column_name_list'] = column_names_list
        request.session['file_name'] = excel_file.name
        return render(request, 'upload.html')


def index(request):
    if request.method == 'GET':
        column_name_list = request.session['column_name_list']
        file_name = request.session['file_name']
        return render(request, 'index.html', {'column_name_list': column_name_list, 'file_name': file_name})


def train_model(request):
    if request.method == 'GET':
        render(request, 'upload.html')
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        json_data = json.loads(raw_data)
        # 从JSON数据中提取相应的字段
        max_depth = int(json_data.get('maxDepth', 0))
        min_samples_split = int(json_data.get('minSamplesSplit', 0))
        min_samples_leaf = int(json_data.get('minSamplesLeaf', 0))
        output_variable = json_data.get('outputVariable', '')
        file_name = request.session.get('file_name', None)
        if file_name is None:
            print('file None')
            return JsonResponse({'error': 'No file name provided'})
        try:
            file_path = f'{settings.MEDIA_ROOT}\\{file_name}'
            print(file_path)
            dataset = pd.read_excel(file_path)
            print(dataset)
        except Exception as e:
            print('excel None')
            return JsonResponse({'error': f'Error loading dataset: {str(e)}'})

        # 分割数据集为训练集和测试集
        X = dataset.drop(columns=[output_variable])
        y = dataset[output_variable]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 创建并训练决策树模型
        clf = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split,
                                     min_samples_leaf=min_samples_leaf)
        clf.fit(X_train, y_train)
        train_model_name_ = file_name[:file_name.index('.')]
        model_filename = f'train_models/{train_model_name_}_decision_tree_model.joblib'
        print(model_filename)
        joblib.dump(clf, model_filename)
        # 在测试集上进行预测并计算准确度
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        # 返回结果
        return JsonResponse({'accuracy': accuracy})

    return HttpResponseBadRequest('Invalid request method')

