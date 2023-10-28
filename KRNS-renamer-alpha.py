import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy, QGroupBox

class DirectoryTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Selected Directory: None', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.label)

        self.btn_select = QPushButton('Select Directory', self)
        self.btn_select.clicked.connect(self.select_directory)
        layout.addWidget(self.btn_select)

        # File Renamer Group
        renamer_group = QGroupBox("LoRA/LyCORIS Files Renamer")
        renamer_layout = QVBoxLayout()

        self.btn_add_modelId = QPushButton('Append the modelId at the start of the file name', self)
        self.btn_add_modelId.clicked.connect(self.add_modelId)
        renamer_layout.addWidget(self.btn_add_modelId)
        self.btn_add_modelId.setToolTip("Adds the modelId before the current file name. For example, 'AwyHandHeartXL.safetensors' becomes '126227_AwyHandHeartXL.safetensors'.")

        self.btn_replace_modelId = QPushButton('Use modelId as the new base file name', self)
        self.btn_replace_modelId.clicked.connect(self.replace_modelId)
        renamer_layout.addWidget(self.btn_replace_modelId)
        self.btn_replace_modelId.setToolTip("Replaces the base file name with the modelId. For example, 'AwyHandHeartXL.safetensors' becomes '126227.safetensors'.")

        self.btn_recover_original_name = QPushButton('Restore the file name to its original form', self)
        self.btn_recover_original_name.clicked.connect(self.recover_original_name)
        renamer_layout.addWidget(self.btn_recover_original_name)
        self.btn_recover_original_name.setToolTip("Restores the file name to its original form as indicated in the .civitai.info file. For example, if original name was 'AwyHandHeartXL', any file starting with the current prefix will be renamed to 'AwyHandHeartXL.safetensors'.")

        renamer_group.setLayout(renamer_layout)
        layout.addWidget(renamer_group)

        self.setLayout(layout)
        self.setWindowTitle('KRN S - Known for Rarity, Niche & Specialized tool')
        self.setMinimumWidth(480)
        self.show()

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.label.setText(f'Selected Directory: {dir_path}')

    def add_modelId(self):
        self.rename_files()

    def replace_modelId(self):
        directory_path = self.label.text().replace('Selected Directory: ', '')
        if directory_path != 'None':
            self.process_directory_for_replace_modelId(directory_path)

    def recover_original_name(self):
        directory_path = self.label.text().replace('Selected Directory: ', '')
        if directory_path != 'None':
            self.process_directory_for_recover_original_name(directory_path)

    def rename_files(self):
        directory_path = self.label.text().replace('Selected Directory: ', '')
        if directory_path != 'None':
            self.process_directory_for_all_files(directory_path)

    def process_directory_for_all_files(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.civitai.info'):
                    file_path = os.path.join(root, file_name)
                    model_id = self.get_model_id_from_info(file_path)
                    prefix = file_name.rsplit('.civitai.info', 1)[0]
                    if model_id:
                        self.rename_files_with_prefix(root, prefix, model_id)

    def process_directory_for_replace_modelId(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.civitai.info'):
                    file_path = os.path.join(root, file_name)
                    model_id = self.get_model_id_from_info(file_path)
                    prefix = file_name.rsplit('.civitai.info', 1)[0]
                    if model_id:
                        self.rename_files_with_modelId(root, prefix, model_id)

    def process_directory_for_recover_original_name(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.civitai.info'):
                    file_path = os.path.join(root, file_name)
                    original_name = self.get_original_name_from_info(file_path)
                    prefix = file_name.rsplit('.civitai.info', 1)[0]
                    if original_name:
                        self.rename_files_with_original_name(root, prefix, original_name)

    def get_model_id_from_info(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('modelId')

    def get_original_name_from_info(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        file_info = data.get('files', [{}])[0]
        original_name = file_info.get('name')
        if original_name:
            return os.path.splitext(original_name)[0]  # Remove file extension
        return None

    def rename_files_with_prefix(self, directory_path, prefix, model_id):
        for file_name in os.listdir(directory_path):
            if file_name.startswith(prefix):
                new_name = f"{model_id}_{file_name}"
                original_path = os.path.join(directory_path, file_name)
                new_path = os.path.join(directory_path, new_name)
                os.rename(original_path, new_path)

    def rename_files_with_modelId(self, directory_path, prefix, model_id):
        for file_name in os.listdir(directory_path):
            if file_name.startswith(prefix):
                new_name = file_name.replace(prefix, str(model_id), 1)
                original_path = os.path.join(directory_path, file_name)
                new_path = os.path.join(directory_path, new_name)
                os.rename(original_path, new_path)

    def rename_files_with_original_name(self, directory_path, prefix, original_name):
        for file_name in os.listdir(directory_path):
            if file_name.startswith(prefix):
                new_name = file_name.replace(prefix, original_name, 1)
                original_path = os.path.join(directory_path, file_name)
                new_path = os.path.join(directory_path, new_name)
                os.rename(original_path, new_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DirectoryTool()
    sys.exit(app.exec_())
