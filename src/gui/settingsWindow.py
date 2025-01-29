from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QHBoxLayout)

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        max_size_label = QLabel("Maximum Size (MB):")
        self.max_size_edit = QLineEdit()
        layout.addWidget(max_size_label)
        layout.addWidget(self.max_size_edit)

        quality_label = QLabel("Recording Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High", "Medium", "Low"])
        layout.addWidget(quality_label)
        layout.addWidget(self.quality_combo)


        button_box = QHBoxLayout() 
        save_button = QPushButton("Save") 
        cancel_button = QPushButton("Cancel")
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)

        layout.addLayout(button_box)

        self.setLayout(layout)

        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)

    def save_settings(self):
        max_size = self.max_size_edit.text() 
        quality = self.quality_combo.currentText()

        self.accept()