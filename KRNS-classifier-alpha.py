import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy, QGroupBox
from collections import defaultdict
import shutil

class DirectoryTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Selected Directory: None', self)
        layout.addWidget(self.label)

        self.btn_select = QPushButton('Select Directory', self)
        self.btn_select.clicked.connect(self.select_directory)
        layout.addWidget(self.btn_select)

        # File Classifier Group
        classifier_group = QGroupBox("LoRA/LyCORIS File Classifier")
        classifier_layout = QVBoxLayout()

        self.btn_sd_version = QPushButton('SD version classifier', self)
        self.btn_sd_version.clicked.connect(self.classify_version)
        self.btn_sd_version.setToolTip("Classifies and moves files in the selected directory based on the SD version.")
        classifier_layout.addWidget(self.btn_sd_version)

        self.btn_nsfw = QPushButton('nsfw classifier', self)
        self.btn_nsfw.clicked.connect(self.nsfw_classifier)
        self.btn_nsfw.setToolTip("Classifies and moves files in the selected directory based on the NSFW rating.")
        classifier_layout.addWidget(self.btn_nsfw)

        # Removed Lora LyCORIS classifier button and related UI code

        classifier_group.setLayout(classifier_layout)
        layout.addWidget(classifier_group)

        self.setLayout(layout)
        self.setWindowTitle('KRN S - Known for Rarity, Niche & Specialized tool')
        self.setMinimumWidth(480)
        self.show()

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.label.setText(f'Selected Directory: {dir_path}')

    def classify_version(self):
        directory_path = self.label.text().replace('Selected Directory: ', '')
        if directory_path != 'None':
            self.sd_version_classifier(directory_path)

    def sd_version_classifier(self, directory):
        base_model_dict = defaultdict(list)

        for filename in os.listdir(directory):
            if filename.endswith('.civitai.info'):
                with open(os.path.join(directory, filename), 'r') as file:
                    data = json.load(file)
                if "baseModel" in data:
                    base_model = data["baseModel"]
                    base_name = filename.replace('.civitai.info', '')
                    related_files = [f for f in os.listdir(directory) if f.startswith(base_name)]
                    base_model_dict[base_model].extend(related_files)

        for base_model, files in base_model_dict.items():
            new_dir = os.path.join(directory, base_model)
            os.makedirs(new_dir, exist_ok=True)
            for file in files:
                shutil.move(os.path.join(directory, file), new_dir)

    def nsfw_classifier(self):
        directory = self.label.text().replace('Selected Directory: ', '')
        if directory != 'None':
            nsfw_dict = defaultdict(list)

            for filename in os.listdir(directory):
                if filename.endswith('.civitai.info'):
                    with open(os.path.join(directory, filename), 'r') as file:
                        data = json.load(file)

                    if "model" in data and isinstance(data["model"], dict) and "nsfw" in data["model"]:
                        nsfw = data["model"]["nsfw"]
                        base_name = filename.replace('.civitai.info', '')
                        related_files = [f for f in os.listdir(directory) if f.startswith(base_name)]
                        nsfw_dict[str(nsfw)].extend(related_files)

            for nsfw, files in nsfw_dict.items():
                new_dir = os.path.join(directory, nsfw)
                os.makedirs(new_dir, exist_ok=True)
                for file in files:
                    shutil.move(os.path.join(directory, file), new_dir)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DirectoryTool()
    sys.exit(app.exec_())
