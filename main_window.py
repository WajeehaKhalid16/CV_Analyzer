"""
Main GUI Window for CV Analyzer
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
import os
import random
import math
sys.path.append('..')

from utils.file_reader import FileReader
from utils.analyzer import CVAnalyzer
from algorithms.brute_force import BruteForce
from algorithms.rabin_karp import RabinKarp
from algorithms.kmp import KMP


class AnimatedBackground(QWidget):
    """Enhanced animated background with multiple effects"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circles = []
        self.particles = []
        self.waves = []
        self.rotation_angle = 0
        self.pulse_scale = 1.0
        self.pulse_direction = 0.01
        
        self.init_circles()
        self.init_particles()
        self.init_waves()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
    
    def init_circles(self):
        
        colors = [
            QColor(102, 126, 234, 80),  
            QColor(118, 75, 162, 80),
            QColor(240, 147, 251, 80),
            QColor(79, 172, 254, 80),
            QColor(56, 239, 125, 80),
        ]
        
        for _ in range(19): 
            x = random.randint(0, 1800)
            y = random.randint(0, 1000)
            radius = random.randint(80, 200)  
            color = random.choice(colors)
            speed_x = random.uniform(-1.2, 1.2)  
            speed_y = random.uniform(-1.2, 1.2)
            
            self.circles.append({
                'x': x, 'y': y, 'radius': radius, 
                'color': color, 'speed_x': speed_x, 'speed_y': speed_y,
                'pulse': random.uniform(0, 3.14)
            })
    
    def init_particles(self):
       
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, 1800),
                'y': random.randint(0, 1000),
                'size': random.randint(2, 6),
                'speed_y': random.uniform(0.3, 1.5),
                'opacity': random.randint(40, 60),
                'color': random.choice([
                    QColor(255, 255, 255),
                    QColor(102, 126, 234),
                    QColor(240, 147, 251),
                ])
            })
    
    def init_waves(self):
        
        for i in range(3):
            self.waves.append({
                'y_offset': i * 150,
                'amplitude': 30,
                'frequency': 0.01,
                'phase': i * 1.0,
                'speed': 0.03,
                'color': QColor(102, 126, 234, 30 + i * 10)
            })
    
    def update_animation(self):
        
        for circle in self.circles:
            circle['x'] += circle['speed_x']
            circle['y'] += circle['speed_y']
            circle['pulse'] += 0.05
            
            if circle['x'] < -circle['radius']:
                circle['x'] = self.width() + circle['radius']
            elif circle['x'] > self.width() + circle['radius']:
                circle['x'] = -circle['radius']
            if circle['y'] < -circle['radius']:
                circle['y'] = self.height() + circle['radius']
            elif circle['y'] > self.height() + circle['radius']:
                circle['y'] = -circle['radius']
        
       
        for particle in self.particles:
            particle['y'] -= particle['speed_y']
            
            if particle['y'] < -10:
                particle['y'] = self.height() + 10
                particle['x'] = random.randint(0, self.width())
        
        
        for wave in self.waves:
            wave['phase'] += wave['speed']
        
        
        self.rotation_angle += 0.5
        self.pulse_scale += self.pulse_direction
        if self.pulse_scale >= 1.3 or self.pulse_scale <= 0.8:
            self.pulse_direction *= -1
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw waves at bottom
        for wave in self.waves:
            path = QPainterPath()
            path.moveTo(0, self.height())
            
            for x in range(0, self.width(), 5):
                y = self.height() - wave['y_offset'] + \
                    wave['amplitude'] * math.sin(wave['frequency'] * x + wave['phase'])
                path.lineTo(x, y)
            
            path.lineTo(self.width(), self.height())
            path.closeSubpath()
            
            painter.setBrush(QBrush(wave['color']))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)
        
        
        for circle in self.circles:
            pulse_factor = 1.0 + 0.2 * math.sin(circle['pulse'])
            radius = int(circle['radius'] * pulse_factor)
            
            
            for i in range(3):
                gradient = QRadialGradient(circle['x'], circle['y'], radius + i * 20)
                color_center = QColor(circle['color'])
                color_center.setAlpha(max(0, circle['color'].alpha() - i * 20))
                color_edge = QColor(circle['color'])
                color_edge.setAlpha(0)
                
                gradient.setColorAt(0, color_center)
                gradient.setColorAt(1, color_edge)
                
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(int(circle['x']), int(circle['y'])), 
                                  radius + i * 20, radius + i * 20)
        
      
            for particle in self.particles:
                color = QColor(particle['color'])
                color.setAlpha(particle['opacity'])
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                
             
                painter.drawEllipse(
                    QPointF(particle['x'], particle['y']),
                    particle['size'], particle['size']
                )
                
         
            if random.random() > 0.97:
                glow_color = QColor(particle['color'])
                glow_color.setAlpha(50)
                painter.setBrush(QBrush(glow_color))
                painter.drawEllipse(
                    QPointF(particle['x'], particle['y']),
                    particle['size'] * 2, particle['size'] * 2
                )

class AnalysisThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, cv_text, job_text, algorithm):
        super().__init__()
        self.cv_text = cv_text
        self.job_text = job_text
        self.algorithm = algorithm
    
    def run(self):
        try:
            self.progress.emit(25)
            text_length = len(self.cv_text)

            analyzer = CVAnalyzer(self.algorithm)
            self.progress.emit(50)

            # Measure execution time (ms)
            import time
            t0 = time.perf_counter()
            results = analyzer.analyze_cv(self.cv_text, self.job_text)
            t1 = time.perf_counter()

            # set measured fields
            results['execution_time'] = (t1 - t0) * 1000.0  # milliseconds
            results['text_length'] = text_length

            total_pattern_length = (
                sum(len(kw) for kw in results.get('mandatory_keywords', [])) +
                sum(len(kw) for kw in results.get('optional_keywords', []))
            )
            results['pattern_length'] = total_pattern_length
            results['num_patterns'] = len(results.get('mandatory_keywords', [])) + len(results.get('optional_keywords', []))

            # ensure comparisons key exists
            if 'comparisons' not in results:
                results['comparisons'] = 0

            self.progress.emit(100)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class BatchAnalysisThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, files, cvs_folder, job_text, algorithm, file_reader):
        super().__init__()
        self.files = files
        self.cvs_folder = cvs_folder
        self.job_text = job_text
        self.algorithm = algorithm
        self.file_reader = file_reader
        
    def run(self):
        try:
            results_list = []
            total_files = len(self.files)

            import time
            for i, filename in enumerate(self.files):
                file_path = os.path.join(self.cvs_folder, filename)
                try:
                    cv_text = self.file_reader.read_file(file_path)
                    text_length = len(cv_text)

                    analyzer = CVAnalyzer(self.algorithm)

                    t0 = time.perf_counter()
                    results = analyzer.analyze_cv(cv_text, self.job_text)
                    t1 = time.perf_counter()

                    # Ensure required fields exist
                    results['execution_time'] = (t1 - t0) * 1000.0  # ms
                    results['filename'] = filename
                    results['text_length'] = text_length

                    total_pattern_length = (
                        sum(len(kw) for kw in results.get('mandatory_keywords', [])) +
                        sum(len(kw) for kw in results.get('optional_keywords', []))
                    )
                    results['pattern_length'] = total_pattern_length
                    results['num_patterns'] = len(results.get('mandatory_keywords', [])) + len(results.get('optional_keywords', []))

                    if 'comparisons' not in results:
                        results['comparisons'] = 0

                    results_list.append(results)

                    progress = int((i + 1) / total_files * 100)
                    self.progress.emit(progress)

                except Exception as e:
                    print(f"Error analyzing {filename}: {str(e)}")

            results_list.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
            self.finished.emit(results_list)

        except Exception as e:
            self.error.emit(str(e))

class CVAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_reader = FileReader()
        self.cv_text = ""
        self.job_text = ""
        self.current_cv_path = ""
        self.performance_history = []
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(" CV Analyzer Pro - Modern Edition")
        
        
        screen = QApplication.desktop().screenGeometry()
        width = int(screen.width() * 0.95)
        height = int(screen.height() * 0.95)
        x = int((screen.width() - width) / 2)
        y = int((screen.height() - height) / 2)
        
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(1000, 600)
        
        
        self.setStyleSheet("""
            QMainWindow {
                background: #0f0f1e;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 14px 20px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 10px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:pressed {
                background: #5a3d7a;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QComboBox {
                padding: 12px;
                border: 2px solid #667eea;
                border-radius: 8px;
                background: #1a1a2e;
                color: white;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox QAbstractItemView {
                background: #1a1a2e;
                color: white;
                selection-background-color: #667eea;
                border: 2px solid #667eea;
            }
            QTextEdit {
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 15px;
                background: #0a0a14;
                color: #f0f0f0;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            QTableWidget {
                border: 2px solid #667eea;
                border-radius: 10px;
                background: #0a0a14;
                gridline-color: #2a2a3e;
                color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid #667eea;
                border-radius: 10px;
                background: #0a0a14;
            }
            QTabBar::tab {
                background: #1a1a2e;
                color: #b0b0b0;
                padding: 12px 20px;
                margin: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
            }
            QProgressBar {
                border: 2px solid #667eea;
                border-radius: 10px;
                text-align: center;
                background: #1a1a2e;
                color: white;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f093fb, stop:0.5 #f5576c, stop:1 #4facfe);
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background: #1a1a2e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #667eea;
                border-radius: 6px;
            }
        """)
        
      
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        
        self.animated_bg = AnimatedBackground(central_widget)
        self.animated_bg.setGeometry(central_widget.rect())
        self.animated_bg.lower()
        
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 10, 12, 10)
        central_widget.setLayout(main_layout)
        
      
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setHandleWidth(4)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #667eea;
            }
            QSplitter::handle:hover {
                background: #764ba2;
            }
        """)
        
        
        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_layout.setSpacing(8)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_widget.setLayout(top_layout)
        
      
        header_frame = QFrame()
        header_frame.setFixedHeight(85)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 10px;
            }
        """)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("CV ANALYZER PRO")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; background: transparent;")
        header_layout.addWidget(title)
        
        subtitle = QLabel(" Advanced String Matching Analytics ")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: white; background: transparent;")
        header_layout.addWidget(subtitle)
        
        header_frame.setLayout(header_layout)
        top_layout.addWidget(header_frame)
        
        # CONTROL PANEL
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # CV Card
        cv_card = self.create_card("#f093fb", "#f5576c")
        cv_layout = QVBoxLayout()
        cv_layout.setSpacing(6)
        cv_layout.setContentsMargins(8, 8, 8, 8)
        
        cv_title = QLabel(" CV Upload")
        cv_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        cv_title.setStyleSheet("color: white;")
        cv_title.setAlignment(Qt.AlignCenter)
        cv_layout.addWidget(cv_title)
        
        self.cv_button = QPushButton("Browse CV")
        self.cv_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cv_button.setMinimumHeight(40)
        self.cv_button.setMaximumHeight(40)
        self.cv_button.setCursor(Qt.PointingHandCursor)
        self.cv_button.clicked.connect(self.browse_cv)
        cv_layout.addWidget(self.cv_button)
        
        self.cv_label = QLabel("No file selected")
        self.cv_label.setFont(QFont("Segoe UI", 9))
        self.cv_label.setStyleSheet("color: rgba(255,255,255,0.9);")
        self.cv_label.setWordWrap(True)
        self.cv_label.setAlignment(Qt.AlignCenter)
        self.cv_label.setMinimumHeight(40)
        cv_layout.addWidget(self.cv_label)
        
        cv_layout.addStretch()
        cv_card.setLayout(cv_layout)
        controls_layout.addWidget(cv_card, 1)
        
        
        job_card = self.create_card("#4facfe", "#00f2fe")
        job_layout = QVBoxLayout()
        job_layout.setSpacing(6)
        job_layout.setContentsMargins(8, 8, 8, 8)
        
        job_title = QLabel(" Job Role")
        job_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        job_title.setStyleSheet("color: white;")
        job_title.setAlignment(Qt.AlignCenter)
        job_layout.addWidget(job_title)
        
        self.job_combo = QComboBox()
        self.job_combo.setFont(QFont("Segoe UI", 10))
        self.job_combo.setMinimumHeight(36)
        self.job_combo.setMaximumHeight(36)
        self.load_job_descriptions()
        job_layout.addWidget(self.job_combo)
        
        self.load_job_button = QPushButton("Load Job")
        self.load_job_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.load_job_button.setMinimumHeight(40)
        self.load_job_button.setMaximumHeight(40)
        self.load_job_button.setCursor(Qt.PointingHandCursor)
        self.load_job_button.clicked.connect(self.load_job_description)
        job_layout.addWidget(self.load_job_button)
        
        job_layout.addStretch()
        job_card.setLayout(job_layout)
        controls_layout.addWidget(job_card, 1)
        
      
        algo_card = self.create_card("#a8edea", "#fed6e3")
        algo_layout = QVBoxLayout()
        algo_layout.setSpacing(6)
        algo_layout.setContentsMargins(8, 8, 8, 8)  
        
        algo_title = QLabel(" ALGORITHMS")  
        algo_title.setFont(QFont("Segoe UI", 12, QFont.Bold))  
        algo_title.setStyleSheet("color: #2d2d44;")
        algo_title.setAlignment(Qt.AlignCenter)
        algo_layout.addWidget(algo_title)
        
        self.algo_combo = QComboBox()
        self.algo_combo.setFont(QFont("Segoe UI", 10))
        self.algo_combo.setMinimumHeight(36)
        self.algo_combo.setMaximumHeight(36)
        self.algo_combo.addItems(["Brute Force", "Rabin-Karp", "KMP"])
        algo_layout.addWidget(self.algo_combo)
        
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
       
        self.analyze_button = QPushButton("ANALYZE\nCV")  
        self.analyze_button.setFont(QFont("Segoe UI", 9, QFont.Bold))  
        self.analyze_button.setMinimumHeight(45)  
        self.analyze_button.setMaximumHeight(45)
        self.analyze_button.setCursor(Qt.PointingHandCursor)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: white;
                border: none;
                padding: 5px 8px;
                font-size: 10px;
                font-weight: bold;
                border-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38ef7d, stop:1 #11998e);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0e7a72, stop:1 #2bc964);
            }
        """)
        self.analyze_button.clicked.connect(self.analyze_cv)
        buttons_layout.addWidget(self.analyze_button)

        
        self.batch_button = QPushButton("RANK\nALL CVs")  
        self.batch_button.setFont(QFont("Segoe UI", 9, QFont.Bold))  
        self.batch_button.setMinimumHeight(45)
        self.batch_button.setMaximumHeight(45)
        self.batch_button.setCursor(Qt.PointingHandCursor)
        self.batch_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f093fb, stop:1 #f5576c);
                color: white;
                border: none;
                padding: 5px 8px;
                font-size: 10px;
                font-weight: bold;
                border-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f5576c, stop:1 #f093fb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d04560, stop:1 #c771d9);
            }
        """)
        self.batch_button.clicked.connect(self.batch_analyze_cvs)
        buttons_layout.addWidget(self.batch_button)
        
       
        algo_layout.addLayout(buttons_layout)
        
        algo_layout.addStretch()
        algo_card.setLayout(algo_layout)
        controls_layout.addWidget(algo_card, 1)
        
   
        top_layout.addLayout(controls_layout)
        
       
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFont(QFont("Segoe UI", 11, QFont.Bold))
        top_layout.addWidget(self.progress_bar)
        
        
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(0)
        results_widget.setLayout(results_layout)
        
    
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
      
        results_tab = QWidget()
        results_tab_layout = QVBoxLayout()
        results_tab_layout.setContentsMargins(8, 8, 8, 8)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Consolas", 10))
        self.results_text.setLineWrapMode(QTextEdit.WidgetWidth)
        results_tab_layout.addWidget(self.results_text)
        
        results_tab.setLayout(results_tab_layout)
        self.tabs.addTab(results_tab, " Results")
        
       
        keywords_tab = QWidget()
        keywords_layout = QVBoxLayout()
        keywords_layout.setContentsMargins(8, 8, 8, 8)
        
        self.keywords_table = QTableWidget()
        self.keywords_table.setColumnCount(3)
        self.keywords_table.setHorizontalHeaderLabels(["KEYWORD", "TYPE", "STATUS"])
        self.keywords_table.horizontalHeader().setStretchLastSection(True)
        self.keywords_table.verticalHeader().setVisible(False)
        keywords_layout.addWidget(self.keywords_table)
        
        keywords_tab.setLayout(keywords_layout)
        self.tabs.addTab(keywords_tab, "🔍 Keywords")
        
        
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout()
        analytics_layout.setContentsMargins(8, 8, 8, 8)
        
        perf_label = QLabel(" Algorithm Performance Comparison")
        perf_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        perf_label.setStyleSheet("color: #f093fb;")
        analytics_layout.addWidget(perf_label)
        
        self.performance_table = QTableWidget()
        self.performance_table.setColumnCount(5)  # Changed from 4 to 5
        self.performance_table.setHorizontalHeaderLabels([
            "Algorithm", "Time (ms)", "Comparisons", "Efficiency (Comp)", "Efficiency (Time)"
        ])

        self.performance_table.horizontalHeader().setStretchLastSection(True)
        self.performance_table.verticalHeader().setVisible(False)
        self.performance_table.setMaximumHeight(140)
        analytics_layout.addWidget(self.performance_table)
        
        self.initialize_performance_table()
        
        charts_label = QLabel("📈 Visual Analytics")
        charts_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        charts_label.setStyleSheet("color: #4facfe;")
        analytics_layout.addWidget(charts_label)
        
        charts_widget = QWidget()
        charts_layout = QHBoxLayout()
        
        self.time_chart = self.create_time_chart()
        charts_layout.addWidget(self.time_chart)
        
        self.comp_chart = self.create_comparisons_chart()
        charts_layout.addWidget(self.comp_chart)
        
        charts_widget.setLayout(charts_layout)
        analytics_layout.addWidget(charts_widget)
        
        analytics_tab.setLayout(analytics_layout)
        self.tabs.addTab(analytics_tab, "⚡ Analytics")
        
        
        details_tab = QWidget()
        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(8, 8, 8, 8)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Consolas", 10))
        self.details_text.setLineWrapMode(QTextEdit.WidgetWidth)
        details_layout.addWidget(self.details_text)
        
        details_tab.setLayout(details_layout)
        self.tabs.addTab(details_tab, " Details")
        
        
        ranking_tab = QWidget()
        ranking_layout = QVBoxLayout()
        ranking_layout.setContentsMargins(8, 8, 8, 8)
        
        ranking_title = QLabel("🏆 Candidate Ranking - All CVs Analyzed")
        ranking_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        ranking_title.setStyleSheet("color: #f093fb; margin-bottom: 10px;")
        ranking_layout.addWidget(ranking_title)
        
        self.ranking_table = QTableWidget()
        self.ranking_table.setColumnCount(6)
        self.ranking_table.setHorizontalHeaderLabels([
            "Rank", "Candidate", "Overall Score", "Mandatory", "Optional", "Status"
        ])
        self.ranking_table.horizontalHeader().setStretchLastSection(True)
        self.ranking_table.verticalHeader().setVisible(False)
        self.ranking_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ranking_table.setSelectionMode(QTableWidget.SingleSelection)
        self.ranking_table.itemDoubleClicked.connect(self.view_candidate_details)
        ranking_layout.addWidget(self.ranking_table)
        
        ranking_tab.setLayout(ranking_layout)
        self.tabs.addTab(ranking_tab, "🏆 Ranking")
        self.ranking_tab = ranking_tab  
        results_layout.addWidget(self.tabs)
        
        
        main_splitter.addWidget(top_widget)
        main_splitter.addWidget(results_widget)
        
      
        main_splitter.setSizes([int(height * 0.25), int(height * 0.75)])
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(main_splitter)
        
       
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-weight: bold;
                padding: 7px;
            }
        """)
        self.statusBar().showMessage(" Ready! Upload CV and select job role.")
    
    def create_card(self, color1, color2):
        card = QFrame()
        card.setMinimumHeight(145)
        card.setMaximumHeight(145)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        return card
    
    def initialize_performance_table(self):
        """Initialize performance table with dual efficiency columns"""
        self.performance_table.setRowCount(3)
        algorithms = ["Brute Force", "Rabin-Karp", "KMP"]
        colors = [QColor("#f5576c"), QColor("#4facfe"), QColor("#38ef7d")]
        
        for row, (algo, color) in enumerate(zip(algorithms, colors)):
            algo_item = QTableWidgetItem(algo)
            algo_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            algo_item.setForeground(color)
            algo_item.setTextAlignment(Qt.AlignCenter)
            self.performance_table.setItem(row, 0, algo_item)
            
            
            for col in range(1, 5):
                item = QTableWidgetItem("N/A")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Segoe UI", 10))
                item.setForeground(QColor("#888888"))
                self.performance_table.setItem(row, col, item)
    
    def update_performance_table(self, results):
        
       
        row_map = {"Brute Force": 0, "Rabin-Karp": 1, "KMP": 2}
        algo_name = results.get('algorithm', 'Unknown')
        if algo_name not in row_map:
            return
        row = row_map[algo_name]

        comparisons_value = results.get('avg_comparisons', results.get('comparisons', 0))
        exec_time = results.get('execution_time', 0.0)

        # Update history
        found = False
        for i, entry in enumerate(self.performance_history):
            if entry['algorithm'] == algo_name:
                self.performance_history[i] = {
                    'algorithm': algo_name,
                    'execution_time': exec_time,
                    'comparisons': int(round(comparisons_value))
                }
                found = True
                break

        if not found:
            self.performance_history.append({
                'algorithm': algo_name,
                'execution_time': exec_time,
                'comparisons': int(round(comparisons_value))
            })

        # Update time cell (Column 1)
        time_item = QTableWidgetItem(f"{exec_time:.4f}")
        time_item.setTextAlignment(Qt.AlignCenter)
        time_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
        time_item.setForeground(QColor("#38ef7d"))
        self.performance_table.setItem(row, 1, time_item)

        # Update comparisons cell (Column 2)
        comp_item = QTableWidgetItem(f"{int(round(comparisons_value)):,}")
        comp_item.setTextAlignment(Qt.AlignCenter)
        comp_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
        comp_item.setForeground(QColor("#4facfe"))
        self.performance_table.setItem(row, 2, comp_item)

        # Check if we have data for ALL three algorithms
        algos_tested = {p['algorithm'] for p in self.performance_history}
        all_algos_tested = {'Brute Force', 'Rabin-Karp', 'KMP'}.issubset(algos_tested)
        
        if all_algos_tested:
            # Get all comparison and time data
            all_comps = [p['comparisons'] for p in self.performance_history 
                        if p.get('comparisons', 0) > 0]
            all_times = [p['execution_time'] for p in self.performance_history 
                        if p.get('execution_time', 0) > 0]
            
            if all_comps and all_times:
                best_comparisons = min(all_comps)  # Fewest comparisons = best
                best_time = min(all_times)  # Fastest time = best
                
                # Update efficiency for ALL three algorithms
                for algo in ['Brute Force', 'Rabin-Karp', 'KMP']:
                    algo_row = row_map[algo]
                    algo_data = next((p for p in self.performance_history 
                                    if p['algorithm'] == algo), None)
                    
                    if algo_data:
                        algo_comps = algo_data.get('comparisons', 0)
                        algo_time = algo_data.get('execution_time', 0)
                        
                        # === COLUMN 3: COMPARISON-BASED EFFICIENCY ===
                        if algo_comps > 0:
                            comp_efficiency = (best_comparisons / algo_comps) * 100.0
                            comp_efficiency = max(1.0, min(100.0, comp_efficiency))
                            
                            comp_eff_text = f"{comp_efficiency:.1f}%"
                            comp_eff_item = QTableWidgetItem(comp_eff_text)
                            comp_eff_item.setTextAlignment(Qt.AlignCenter)
                            comp_eff_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                            
                            # Color based on comparison efficiency
                            if comp_efficiency >= 95:
                                comp_eff_item.setForeground(QColor("#38ef7d"))  # Green
                            elif comp_efficiency >= 80:
                                comp_eff_item.setForeground(QColor("#4facfe"))  # Blue
                            elif comp_efficiency >= 50:
                                comp_eff_item.setForeground(QColor("#f093fb"))  # Purple
                            else:
                                comp_eff_item.setForeground(QColor("#f5576c"))  # Red
                            
                            self.performance_table.setItem(algo_row, 3, comp_eff_item)
                        
                        # === COLUMN 4: TIME-BASED EFFICIENCY ===
                        if algo_time > 0:
                            time_efficiency = (best_time / algo_time) * 100.0
                            time_efficiency = max(1.0, min(100.0, time_efficiency))
                            
                            time_eff_text = f"{time_efficiency:.1f}%"
                            time_eff_item = QTableWidgetItem(time_eff_text)
                            time_eff_item.setTextAlignment(Qt.AlignCenter)
                            time_eff_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                            
                            # Color based on time efficiency
                            if time_efficiency >= 95:
                                time_eff_item.setForeground(QColor("#38ef7d"))  # Green
                            elif time_efficiency >= 80:
                                time_eff_item.setForeground(QColor("#4facfe"))  # Blue
                            elif time_efficiency >= 50:
                                time_eff_item.setForeground(QColor("#f093fb"))  # Purple
                            else:
                                time_eff_item.setForeground(QColor("#f5576c"))  # Red
                            
                            self.performance_table.setItem(algo_row, 4, time_eff_item)
        else:
            # Show "N/A" for both efficiency columns until all algorithms tested
            for col in [3, 4]:  # Both efficiency columns
                eff_item = QTableWidgetItem("N/A")
                eff_item.setTextAlignment(Qt.AlignCenter)
                eff_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                eff_item.setForeground(QColor("#888888"))  # Gray
                self.performance_table.setItem(row, col, eff_item)
        
        self.performance_table.viewport().update()

    

    def create_time_chart(self):
        chart = QChart()
        chart.setTitle("⏱️ Execution Time")
        chart.setBackgroundBrush(QBrush(QColor("#0a0a14")))
        chart.setTitleBrush(QBrush(QColor("#ffffff")))
        
        bar_set = QBarSet("Time (ms)")
        bar_set.append([0, 0, 0])
        bar_set.setColor(QColor("#667eea"))
        
        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)
        
        axis_x = QBarCategoryAxis()
        axis_x.append(["BF", "RK", "KMP"])
        axis_x.setLabelsColor(QColor("#ffffff"))
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 1)
        axis_y.setLabelsColor(QColor("#ffffff"))
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(False)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        self.time_bar_set = bar_set
        self.time_axis_y = axis_y
        
        return chart_view
    
    def create_comparisons_chart(self):
        chart = QChart()
        chart.setTitle(" Comparisons")
        chart.setBackgroundBrush(QBrush(QColor("#0a0a14")))
        chart.setTitleBrush(QBrush(QColor("#ffffff")))
        
        bar_set = QBarSet("Count")
        bar_set.append([0, 0, 0])
        bar_set.setColor(QColor("#f093fb"))
        
        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)
        
        axis_x = QBarCategoryAxis()
        axis_x.append(["BF", "RK", "KMP"])
        axis_x.setLabelsColor(QColor("#ffffff"))
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setLabelsColor(QColor("#ffffff"))
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(False)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        self.comp_bar_set = bar_set
        self.comp_axis_y = axis_y
        
        return chart_view
    
    def update_charts(self, results):
        """
        Update charts with current algorithm results
        """
        # Remove old entry for this algorithm
        self.performance_history = [
            r for r in self.performance_history if r['algorithm'] != results['algorithm']
        ]
        
        # Add current result
        perf_data = {
            'algorithm': results['algorithm'],
            'execution_time': results['execution_time'],
            'comparisons': results['comparisons']
        }
        self.performance_history.append(perf_data)
        
        # Update performance table
        self.update_performance_table(results)
        
        # Get latest data for each algorithm
        bf_result = next((r for r in self.performance_history if r['algorithm'] == 'Brute Force'), None)
        rk_result = next((r for r in self.performance_history if r['algorithm'] == 'Rabin-Karp'), None)
        kmp_result = next((r for r in self.performance_history if r['algorithm'] == 'KMP'), None)
        
        bf_time = bf_result['execution_time'] if bf_result else 0
        rk_time = rk_result['execution_time'] if rk_result else 0
        kmp_time = kmp_result['execution_time'] if kmp_result else 0
        
        bf_comp = bf_result['comparisons'] if bf_result else 0
        rk_comp = rk_result['comparisons'] if rk_result else 0
        kmp_comp = kmp_result['comparisons'] if kmp_result else 0
        
        # Update time chart
        self.time_bar_set.remove(0, 3)
        self.time_bar_set.append([bf_time, rk_time, kmp_time])
        
        max_time = max(bf_time, rk_time, kmp_time)
        if max_time > 0:
            self.time_axis_y.setRange(0, max_time * 1.2)
        else:
            self.time_axis_y.setRange(0, 1)
        
        # Update comparisons chart
        self.comp_bar_set.remove(0, 3)
        self.comp_bar_set.append([bf_comp, rk_comp, kmp_comp])
        
        max_comp = max(bf_comp, rk_comp, kmp_comp)
        if max_comp > 0:
            self.comp_axis_y.setRange(0, max_comp * 1.2)
        else:
            self.comp_axis_y.setRange(0, 100)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'animated_bg'):
            self.animated_bg.setGeometry(self.centralWidget().rect())
    
    def load_job_descriptions(self):
        job_folder = "data/job_descriptions"
        if os.path.exists(job_folder):
            files = [f for f in os.listdir(job_folder) if f.endswith('.txt')]
            for file in files:
                name = file.replace('.txt', '').replace('_', ' ').title()
                self.job_combo.addItem(name, file)
    
    def browse_cv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CV", "data/cvs", "Documents (*.pdf *.docx *.txt)"
        )
        
        if file_path:
            try:
                self.cv_text = self.file_reader.read_file(file_path)
                self.current_cv_path = file_path
                filename = os.path.basename(file_path)
                
                
                self.performance_history.clear()
                self.initialize_performance_table()
                
              
                self.time_bar_set.remove(0, 3)
                self.time_bar_set.append([0, 0, 0])
                self.time_axis_y.setRange(0, 1)
                
                self.comp_bar_set.remove(0, 3)
                self.comp_bar_set.append([0, 0, 0])
                self.comp_axis_y.setRange(0, 100)
                
                self.cv_label.setText(f" {filename}")
                self.cv_label.setStyleSheet("color: white; font-weight: bold; font-size: 10px;")
                self.statusBar().showMessage(f" CV Loaded: {filename} | Analytics Reset")
            except Exception as e:
                self.show_styled_message("Error", f"Failed to read CV:\n{str(e)}", "error")
    
    def load_job_description(self):
        if self.job_combo.currentIndex() == -1:
            self.show_styled_message("Warning", "Please select a job role from the dropdown!", "warning")
            return
        
        filename = self.job_combo.currentData()
        file_path = os.path.join("data/job_descriptions", filename)
        
        try:
            self.job_text = self.file_reader.read_file(file_path)
            self.statusBar().showMessage(f" Job: {self.job_combo.currentText()}")
            self.show_styled_message("Success", 
                f"Job Description Loaded Successfully!\n\n📋 Position: {self.job_combo.currentText()}", 
                "success")
        except Exception as e:
            self.show_styled_message("Error", f"Failed to load job description:\n\n{str(e)}", "error")
    
    def show_styled_message(self, title, message, msg_type):
        """Show beautiful styled message dialogs"""
        msg = QMessageBox(self)
        
        if msg_type == "error":
            msg.setIcon(QMessageBox.Critical)
            title = f" {title}"
            button_colors = "stop:0 #f5576c, stop:1 #f093fb"
        elif msg_type == "warning":
            msg.setIcon(QMessageBox.Warning)
            title = f" {title}"
            button_colors = "stop:0 #ffecd2, stop:1 #fcb69f"
        else:  # success
            msg.setIcon(QMessageBox.Information)
            title = f" {title}"
            button_colors = "stop:0 #11998e, stop:1 #38ef7d"
        
        msg.setWindowTitle(title)
        msg.setText(message)
        
        # Beautiful styling
        msg.setStyleSheet(f"""
            QMessageBox {{
                background: #1a1a2e;
            }}
            QMessageBox QLabel {{
                color: white;
                font-size: 13px;
                font-weight: bold;
                min-width: 450px;
                min-height: 70px;
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    {button_colors});
                color: {'white' if msg_type != 'warning' else '#2d2d44'};
                border-radius: 8px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 12px;
                min-width: 100px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    {button_colors.replace('stop:0', 'stop:1').replace('stop:1', 'stop:0', 1)});
            }}
        """)
        msg.exec_()
    
    def get_selected_algorithm(self):
        algo_name = self.algo_combo.currentText()
        if algo_name == "Brute Force":
            return BruteForce()
        elif algo_name == "Rabin-Karp":
            return RabinKarp()
        else:
            return KMP()
    
    def analyze_cv(self):
        if not self.cv_text:
            self.show_styled_message("Warning", 
                "Please select a CV file first!\n\nClick 'Browse CV' to upload a resume.", 
                "warning")
            return
        
        if not self.job_text:
            self.show_styled_message("Warning", 
                "Please load a job description first!\n\nSelect a job role and click 'Load Job'.", 
                "warning")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage(" Analyzing...")
        self.analyze_button.setEnabled(False)
        self.analyze_button.setText(" Analyzing...")
        
        algorithm = self.get_selected_algorithm()
        
        self.analysis_thread = AnalysisThread(self.cv_text, self.job_text, algorithm)
        self.analysis_thread.finished.connect(self.display_results)
        self.analysis_thread.error.connect(self.show_error)
        self.analysis_thread.progress.connect(self.progress_bar.setValue)
        self.analysis_thread.start()
    
    def display_results(self, results):
        """
        Modified display_results to ensure lengths are stored
        """
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("ANALYZE\nCV")
        self.statusBar().showMessage(" Analysis Complete!")
        
        # STORE lengths for efficiency calculation
        results['text_length'] = len(self.cv_text)
        
        # Calculate total pattern length
        total_pattern_length = (
            sum(len(kw) for kw in results['mandatory_keywords']) +
            sum(len(kw) for kw in results['optional_keywords'])
        )
        results['pattern_length'] = total_pattern_length
        results['num_patterns'] = len(results['mandatory_keywords']) + len(results['optional_keywords'])
        
        filename = os.path.basename(self.current_cv_path)
    
    
        
        # Tab 1: Results
        result_text = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                          CV ANALYSIS REPORT                           ║
╚═══════════════════════════════════════════════════════════════════════╝

📄 CANDIDATE: {filename}
💼 POSITION: {self.job_combo.currentText()}
⚙️ ALGORITHM: {results['algorithm']}

╔═══════════════════════════════════════════════════════════════════════╗
║                     🌟 OVERALL MATCH SCORE 🌟                        ║
╚═══════════════════════════════════════════════════════════════════════╝

                           {results['overall_score']:.1f}%
                            
    Mandatory: {results['mandatory_score']:.1f}%  |  ✨ Optional: {results['optional_score']:.1f}%

╔═══════════════════════════════════════════════════════════════════════╗
║          MANDATORY SKILLS ({len(results['mandatory_found'])}/{len(results['mandatory_keywords'])})                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

 FOUND ({len(results['mandatory_found'])} skills):
"""
        
        if results['mandatory_found']:
            for skill in results['mandatory_found']:
                result_text += f"   • {skill}\n"
        else:
            result_text += "   None\n"
        
        result_text += f"\n MISSING ({len(results['mandatory_missing'])} skills):\n"
        
        if results['mandatory_missing']:
            for skill in results['mandatory_missing']:
                result_text += f"   • {skill}\n"
        else:
            result_text += "   None\n"
        
        result_text += f"""
╔═══════════════════════════════════════════════════════════════════════╗
║        ✨ OPTIONAL SKILLS ({len(results['optional_found'])}/{len(results['optional_keywords'])})                                        ║
╚═══════════════════════════════════════════════════════════════════════╝

 FOUND ({len(results['optional_found'])} skills):
"""
        
        if results['optional_found']:
            for skill in results['optional_found']:
                result_text += f"   • {skill}\n"
        else:
            result_text += "   None\n"
        
        result_text += f"\n MISSING ({len(results['optional_missing'])} skills):\n"
        
        if results['optional_missing']:
            for skill in results['optional_missing']:
                result_text += f"   • {skill}\n"
        else:
            result_text += "   None\n"
        
        result_text += """
╔═══════════════════════════════════════════════════════════════════════╗
║                     🎖️ RECOMMENDATION 🎖️                            ║
╚═══════════════════════════════════════════════════════════════════════╝

"""
        
        if results['overall_score'] >= 80:
            result_text += "🌟 EXCELLENT MATCH! Highly qualified candidate! 🌟\n"
        elif results['overall_score'] >= 60:
            result_text += " GOOD MATCH! Meets most requirements! \n"
        elif results['overall_score'] >= 40:
            result_text += "⚠️ MODERATE MATCH. Has some relevant skills.\n"
        else:
            result_text += " LOW MATCH. Lacks many required skills.\n"
        
        result_text += "\n" + "═" * 71 + "\n"
        result_text += "              ✨ CV Analyzer Pro ✨\n"
        result_text += "═" * 71
        
        self.results_text.setText(result_text)
        
 
        self.populate_keywords_table(results)
        self.update_charts(results)  # This will now have correct data
        self.create_details_text(results)
        
        self.tabs.setCurrentIndex(0)
    
    def populate_keywords_table(self, results):
        total = len(results['mandatory_keywords']) + len(results['optional_keywords'])
        self.keywords_table.setRowCount(total)
        
        row = 0
        for keyword in results['mandatory_keywords']:
            self.keywords_table.setItem(row, 0, QTableWidgetItem(keyword))
            
            type_item = QTableWidgetItem("💎 MANDATORY")
            type_item.setForeground(QColor(240, 147, 251))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 1, type_item)
            
            if keyword in results['mandatory_found']:
                status_item = QTableWidgetItem(" FOUND")
                status_item.setForeground(QColor(56, 239, 125))
            else:
                status_item = QTableWidgetItem(" MISSING")
                status_item.setForeground(QColor(245, 87, 108))
            
            status_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 2, status_item)
            row += 1
        
        for keyword in results['optional_keywords']:
            self.keywords_table.setItem(row, 0, QTableWidgetItem(keyword))
            
            type_item = QTableWidgetItem("✨ OPTIONAL")
            type_item.setForeground(QColor(79, 172, 254))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 1, type_item)
            
            if keyword in results['optional_found']:
                status_item = QTableWidgetItem(" FOUND")
                status_item.setForeground(QColor(56, 239, 125))
            else:
                status_item = QTableWidgetItem(" MISSING")
                status_item.setForeground(QColor(150, 150, 150))
            
            status_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 2, status_item)
            row += 1
        
        self.keywords_table.resizeColumnsToContents()
    
    def create_details_text(self, results):
        details = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                   ⚡ PERFORMANCE METRICS ⚡                           ║
╚═══════════════════════════════════════════════════════════════════════╝

ALGORITHM: {results['algorithm']}

⏱️  EXECUTION TIME: {results['execution_time']:.4f} milliseconds
🔢 CHARACTER COMPARISONS: {results['comparisons']:,}
📊 KEYWORDS ANALYZED: {len(results['mandatory_keywords']) + len(results['optional_keywords'])}
📄 CV SIZE: {len(self.cv_text):,} characters

╔═══════════════════════════════════════════════════════════════════════╗
║                      ALGORITHM INFORMATION                             ║
╚═══════════════════════════════════════════════════════════════════════╝

"""
        
        if results['algorithm'] == "Brute Force":
            details += """
  BRUTE FORCE ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
  • Simple character-by-character comparison
  • Checks every position sequentially
  • No preprocessing required

TIME COMPLEXITY: O(n × m)
SPACE COMPLEXITY: O(1)

ADVANTAGES:
  - Very simple to implement
  - Works well for small texts
  - No preprocessing overhead

DISADVANTAGES:
  - Can be slow for large texts
  - Many redundant comparisons

BEST USE: Short documents, single keyword searches
"""
        elif results['algorithm'] == "Rabin-Karp":
            details += """
  RABIN-KARP ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
  • Uses rolling hash function for pattern matching
  • Computes hash values and compares them
  • Only does character comparison when hashes match

TIME COMPLEXITY: O(n + m) average case
SPACE COMPLEXITY: O(1)

ADVANTAGES:
  - Fast average-case performance
  - Excellent for multiple pattern searches
  - Efficient rolling hash technique

DISADVANTAGES:
  - Potential hash collisions
  - Worst-case can be slow

BEST USE: Multiple keyword matching, large documents
"""
        else:
            details += """
   KMP (KNUTH-MORRIS-PRATT) ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
  • Uses preprocessing to build failure function (LPS array)
  • Never backtracks in the main text
  • Skips unnecessary comparisons intelligently

TIME COMPLEXITY: O(n + m) - Guaranteed!
SPACE COMPLEXITY: O(m)

ADVANTAGES:
  - Guaranteed O(n + m) performance
  - Never backtracks in text
  - Very efficient for long patterns
  - Industry-standard algorithm

DISADVANTAGES:
  - Requires preprocessing
  - More complex to implement
  - Extra memory for LPS array

BEST USE: Production systems, large CV documents
"""
        
        details += """

╔═══════════════════════════════════════════════════════════════════════╗
║                  🏆 ALGORITHM COMPARISON 🏆                          ║
╚═══════════════════════════════════════════════════════════════════════╝

  ALGORITHM      | TIME          | SPACE | BEST FOR
  ───────────────┼───────────────┼───────┼─────────────────────
  Brute Force    | O(n × m)      | O(1)  | Small texts
  Rabin-Karp     | O(n+m) avg    | O(1)  | Multiple patterns
  KMP            | O(n+m)        | O(m)  | Long patterns

═══════════════════════════════════════════════════════════════════════
            Thank you for using CV Analyzer Pro!  
═══════════════════════════════════════════════════════════════════════
"""
        
        self.details_text.setText(details)
    
    def show_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("ANALYZE\nCV")
        self.statusBar().showMessage(" Analysis failed!")
        self.show_styled_message("Error", f"An error occurred during analysis:\n\n{error_msg}", "error")

    def batch_analyze_cvs(self):
        """Analyze all CVs in folder and rank them"""
        
        if not self.job_text:
            self.show_styled_message("Warning", 
                "Please load a job description first!\n\nSelect a job role and click 'Load Job'.", 
                "warning")
            return
        
        # Get all CV files
        cvs_folder = "data/cvs"
        if not os.path.exists(cvs_folder):
            self.show_styled_message("Error", 
                "CVs folder not found!\n\nPlease create 'data/cvs' folder.", 
                "error")
            return
        
        files = [f for f in os.listdir(cvs_folder) 
                 if f.lower().endswith(('.pdf', '.docx', '.txt'))]
        
        if not files:
            self.show_styled_message("Warning", 
                f"No CV files found in '{cvs_folder}' folder!\n\nPlease add PDF, DOCX, or TXT files.", 
                "warning")
            return
        
        # Show progress
        self.statusBar().showMessage(f" Analyzing {len(files)} CVs...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.batch_button.setEnabled(False)
        self.batch_button.setText("⏳ Analyzing...")
        
        # Get selected algorithm
        algorithm = self.get_selected_algorithm()
        
        # Start batch analysis thread
        self.batch_thread = BatchAnalysisThread(
            files, cvs_folder, self.job_text, algorithm, self.file_reader
        )
        self.batch_thread.finished.connect(self.display_batch_results)
        self.batch_thread.error.connect(self.show_batch_error)
        self.batch_thread.progress.connect(self.progress_bar.setValue)
        self.batch_thread.start()
    
    def display_batch_results(self, results_list):
        """Display results after batch analysis completes"""
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.batch_button.setEnabled(True)
        self.batch_button.setText("RANK\nALL CVs")
        
        if not results_list:
            self.show_styled_message("Warning", 
                "No CVs were successfully analyzed.", 
                "warning")
            self.statusBar().showMessage(" No results")
            return
        
    
        self.display_ranked_results(results_list)
        self.display_batch_analytics(results_list)
        self.update_batch_analytics(results_list)  
        
        self.statusBar().showMessage(
            f" Analyzed and ranked {len(results_list)} candidates!"
        )
        
       
        self.tabs.setCurrentWidget(self.ranking_tab)
    def show_batch_error(self, error_msg):
        """Handle batch analysis errors"""
        self.progress_bar.setVisible(False)
        self.batch_button.setEnabled(True)
        self.batch_button.setText("RANK\nALL CVs")
        self.statusBar().showMessage(" Batch analysis failed!")
        self.show_styled_message("Error", 
            f"An error occurred during batch analysis:\n\n{error_msg}", 
            "error")
        
    def update_batch_analytics(self, results_list):
        if not results_list:
            return

        total_cvs = len(results_list)
        total_time = sum(r.get('execution_time', 0) for r in results_list)
        total_comparisons = sum(r.get('comparisons', 0) for r in results_list)

        avg_time = total_time / total_cvs if total_cvs else 0.0
        avg_comparisons = total_comparisons / total_cvs if total_cvs else 0.0

        avg_text_length = int(sum(r.get('text_length', 0) for r in results_list) / total_cvs) if total_cvs else 0
        avg_pattern_length = int(sum(r.get('pattern_length', 0) for r in results_list) / total_cvs) if total_cvs else 0

        algo_name = results_list[0].get('algorithm', 'Unknown')

        batch_result = {
            'algorithm': algo_name,
            'execution_time': avg_time,
            'avg_comparisons': int(round(avg_comparisons)),
            'total_comparisons': int(total_comparisons),
            'text_length': avg_text_length,
            'pattern_length': avg_pattern_length,
            'num_patterns': results_list[0].get('num_patterns', 0)
        }


        found = False
        for i, entry in enumerate(self.performance_history):
            if entry['algorithm'] == algo_name:
                self.performance_history[i] = {
                    'algorithm': algo_name,
                    'execution_time': avg_time,
                    'comparisons': int(round(avg_comparisons))
                }
                found = True
                break

        if not found:
            self.performance_history.append({
                'algorithm': algo_name,
                'execution_time': avg_time,
                'comparisons': int(round(avg_comparisons))
            })

        self.update_performance_table(batch_result)
        self._update_charts_from_history()


    def _update_charts_from_history(self):
        """Helper to update charts from performance history"""
        bf_result = next((p for p in self.performance_history if p['algorithm'] == 'Brute Force'), None)
        rk_result = next((p for p in self.performance_history if p['algorithm'] == 'Rabin-Karp'), None)
        kmp_result = next((p for p in self.performance_history if p['algorithm'] == 'KMP'), None)
        
        bf_time = bf_result['execution_time'] if bf_result else 0
        rk_time = rk_result['execution_time'] if rk_result else 0
        kmp_time = kmp_result['execution_time'] if kmp_result else 0
        
        bf_comp = bf_result['comparisons'] if bf_result else 0
        rk_comp = rk_result['comparisons'] if rk_result else 0
        kmp_comp = kmp_result['comparisons'] if kmp_result else 0
        
       
        self.time_bar_set.remove(0, 3)
        self.time_bar_set.append([bf_time, rk_time, kmp_time])
        max_time = max(bf_time, rk_time, kmp_time)
        self.time_axis_y.setRange(0, max_time * 1.2 if max_time > 0 else 1)
        
        self.comp_bar_set.remove(0, 3)
        self.comp_bar_set.append([bf_comp, rk_comp, kmp_comp])
        max_comp = max(bf_comp, rk_comp, kmp_comp)
        self.comp_axis_y.setRange(0, max_comp * 1.2 if max_comp > 0 else 100)
    def display_ranked_results(self, results_list):
        """Display ranked list of candidates in table"""
        
        self.ranking_table.setRowCount(len(results_list))
        
        for rank, results in enumerate(results_list, 1):
            # Rank
            rank_item = QTableWidgetItem(f"#{rank}")
            rank_item.setTextAlignment(Qt.AlignCenter)
            rank_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            if rank == 1:
                rank_item.setForeground(QColor("#FFD700"))  # Gold
            elif rank == 2:
                rank_item.setForeground(QColor("#C0C0C0"))  # Silver
            elif rank == 3:
                rank_item.setForeground(QColor("#CD7F32"))  # Bronze
            else:
                rank_item.setForeground(QColor("#4facfe"))
            self.ranking_table.setItem(rank - 1, 0, rank_item)
            
            # Candidate name
            name_item = QTableWidgetItem(results['filename'])
            name_item.setFont(QFont("Segoe UI", 10))
            self.ranking_table.setItem(rank - 1, 1, name_item)
        
            score_item = QTableWidgetItem(f"{results['overall_score']:.1f}%")
            score_item.setTextAlignment(Qt.AlignCenter)
            score_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            
            if results['overall_score'] >= 80:
                score_item.setForeground(QColor("#38ef7d"))  # Green - Excellent
                status = "⭐ EXCELLENT"
                status_color = QColor("#38ef7d")
            elif results['overall_score'] >= 60:
                score_item.setForeground(QColor("#4facfe"))  # Blue - Good
                status = " GOOD"
                status_color = QColor("#4facfe")
            elif results['overall_score'] >= 40:
                score_item.setForeground(QColor("#f093fb"))  # Purple - Fair
                status = " FAIR"
                status_color = QColor("#f093fb")
            else:
                score_item.setForeground(QColor("#f5576c"))  
                status = " POOR"
                status_color = QColor("#f5576c")
            
            self.ranking_table.setItem(rank - 1, 2, score_item)
            
            
            mand_item = QTableWidgetItem(f"{results['mandatory_score']:.1f}%")
            mand_item.setTextAlignment(Qt.AlignCenter)
            mand_item.setFont(QFont("Segoe UI", 10))
            mand_item.setForeground(QColor("#f093fb"))
            self.ranking_table.setItem(rank - 1, 3, mand_item)
            
           
            opt_item = QTableWidgetItem(f"{results['optional_score']:.1f}%")
            opt_item.setTextAlignment(Qt.AlignCenter)
            opt_item.setFont(QFont("Segoe UI", 10 ))
            opt_item.setForeground(QColor("#4facfe"))
            self.ranking_table.setItem(rank - 1, 4, opt_item)
            
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            status_item.setForeground(status_color)
            self.ranking_table.setItem(rank - 1, 5, status_item)
        
        
        self.ranking_table.resizeColumnsToContents()
    
    def display_batch_analytics(self, results_list):
        """Display aggregate analytics for all CVs"""
        
       
        total_cvs = len(results_list)
        avg_score = sum(r['overall_score'] for r in results_list) / total_cvs
        avg_mandatory = sum(r['mandatory_score'] for r in results_list) / total_cvs
        avg_optional = sum(r['optional_score'] for r in results_list) / total_cvs
        
        excellent = sum(1 for r in results_list if r['overall_score'] >= 80)
        good = sum(1 for r in results_list if 60 <= r['overall_score'] < 80)
        fair = sum(1 for r in results_list if 40 <= r['overall_score'] < 60)
        poor = sum(1 for r in results_list if r['overall_score'] < 40)
        
        summary_text = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                  BATCH ANALYSIS SUMMARY - ALL CVs                     ║
╚═══════════════════════════════════════════════════════════════════════╝

📊 TOTAL CANDIDATES ANALYZED: {total_cvs}
💼 POSITION: {self.job_combo.currentText()}
⚙️ ALGORITHM: {results_list[0]['algorithm']}

╔═══════════════════════════════════════════════════════════════════════╗
║                    AGGREGATE STATISTICS                               ║
╚═══════════════════════════════════════════════════════════════════════╝

 AVERAGE OVERALL SCORE: {avg_score:.1f}%
 AVERAGE MANDATORY MATCH: {avg_mandatory:.1f}%
 AVERAGE OPTIONAL MATCH: {avg_optional:.1f}%

╔═══════════════════════════════════════════════════════════════════════╗
║                 🏆 CANDIDATE DISTRIBUTION 🏆                         ║
╚═══════════════════════════════════════════════════════════════════════╝

⭐ EXCELLENT (80%+):  {excellent} candidates ({excellent/total_cvs*100:.1f}%)
 GOOD (60-79%):     {good} candidates ({good/total_cvs*100:.1f}%)
  FAIR (40-59%):     {fair} candidates ({fair/total_cvs*100:.1f}%)
 POOR (<40%):       {poor} candidates ({poor/total_cvs*100:.1f}%)

╔═══════════════════════════════════════════════════════════════════════╗
║                    🌟 TOP 5 CANDIDATES 🌟                           ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
        
        for i, result in enumerate(results_list[:5], 1):
            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            summary_text += f"""
{medal} RANK #{i}: {result['filename']}
   Overall: {result['overall_score']:.1f}% | Mandatory: {result['mandatory_score']:.1f}% | Optional: {result['optional_score']:.1f}%
"""
        
        summary_text += "\n" + "═" * 71
        
        self.results_text.setText(summary_text)
        
        
        self.populate_aggregate_keywords(results_list)
        
    
        self.create_batch_details(results_list)
    
    def populate_aggregate_keywords(self, results_list):
        """Show which keywords were most/least found across all CVs"""
        
      
        mandatory_counts = {}
        optional_counts = {}
        
        for result in results_list:
            for kw in result['mandatory_found']:
                mandatory_counts[kw] = mandatory_counts.get(kw, 0) + 1
            for kw in result['optional_found']:
                optional_counts[kw] = optional_counts.get(kw, 0) + 1
        
       
        all_mandatory = results_list[0]['mandatory_keywords']
        all_optional = results_list[0]['optional_keywords']
        
        total_cvs = len(results_list)
        
      
        self.keywords_table.setRowCount(len(all_mandatory) + len(all_optional))
        
        row = 0
       
        for keyword in all_mandatory:
            count = mandatory_counts.get(keyword, 0)
            percentage = (count / total_cvs) * 100
            
            kw_item = QTableWidgetItem(keyword)
            self.keywords_table.setItem(row, 0, kw_item)
            
            type_item = QTableWidgetItem("💎 MANDATORY")
            type_item.setForeground(QColor(240, 147, 251))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 1, type_item)
            
            status_item = QTableWidgetItem(f"{count}/{total_cvs} CVs ({percentage:.0f}%)")
            status_item.setTextAlignment(Qt.AlignCenter)
            
            if percentage >= 70:
                status_item.setForeground(QColor(56, 239, 125))  
            elif percentage >= 40:
                status_item.setForeground(QColor(79, 172, 254))  
            else:
                status_item.setForeground(QColor(245, 87, 108))  
            
            self.keywords_table.setItem(row, 2, status_item)
            row += 1
        
        
        for keyword in all_optional:
            count = optional_counts.get(keyword, 0)
            percentage = (count / total_cvs) * 100
            
            kw_item = QTableWidgetItem(keyword)
            self.keywords_table.setItem(row, 0, kw_item)
            
            type_item = QTableWidgetItem("✨ OPTIONAL")
            type_item.setForeground(QColor(79, 172, 254))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.keywords_table.setItem(row, 1, type_item)
            
            status_item = QTableWidgetItem(f"{count}/{total_cvs} CVs ({percentage:.0f}%)")
            status_item.setTextAlignment(Qt.AlignCenter)
            
            if percentage >= 50:
                status_item.setForeground(QColor(56, 239, 125))
            elif percentage >= 25:
                status_item.setForeground(QColor(150, 150, 150))
            else:
                status_item.setForeground(QColor(100, 100, 100))
            
            self.keywords_table.setItem(row, 2, status_item)
            row += 1
        
        self.keywords_table.resizeColumnsToContents()
    
    def create_batch_details(self, results_list):
        total_cvs = len(results_list)
        total_time = sum(r.get('execution_time', 0) for r in results_list)
        total_comparisons = sum(r.get('comparisons', 0) for r in results_list)
        avg_time = total_time / total_cvs if total_cvs else 0.0
        avg_comparisons = total_comparisons / total_cvs if total_cvs else 0.0

        details = f"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                BATCH PERFORMANCE METRICS                              ║
    ╚═══════════════════════════════════════════════════════════════════════╝

    ALGORITHM: {results_list[0].get('algorithm', 'Unknown')}

    TOTAL CVs ANALYZED: {total_cvs}
    TOTAL EXECUTION TIME: {total_time:.2f} ms
    AVERAGE TIME PER CV: {avg_time:.4f} ms
    TOTAL COMPARISONS (ALL CVs): {total_comparisons:,}
    AVG COMPARISONS PER CV: {avg_comparisons:,.0f}

    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                     PROCESSING EFFICIENCY                             ║
    ╚═══════════════════════════════════════════════════════════════════════╝

    FASTEST CV: {min(r.get('execution_time', 0) for r in results_list):.4f} ms
    SLOWEST CV: {max(r.get('execution_time', 0) for r in results_list):.4f} ms
    THROUGHPUT: {(total_cvs / total_time * 1000):.1f} CVs/second

    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                       RECOMMENDATION INSIGHTS                         ║
    ╚═══════════════════════════════════════════════════════════════════════╝

    - The {results_list[0]['algorithm']} algorithm processed all CVs efficiently
    - Top candidate: {results_list[0]['filename']} with {results_list[0]['overall_score']:.1f}% match
    - Consider shortlisting candidates with 60%+ overall score
    - Review mandatory skills for candidates below threshold

    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                     ALGORITHM INFORMATION                             ║
    ╚═══════════════════════════════════════════════════════════════════════╝

    """
        
        if results_list[0]['algorithm'] == "Brute Force":
            details += """
    🔹 BRUTE FORCE ALGORITHM
    ────────────────────────────────────────────────────────────────────

    DESCRIPTION:
    • Simple character-by-character comparison
    • Checks every position sequentially
    • No preprocessing required

    TIME COMPLEXITY: O(n × m)
    SPACE COMPLEXITY: O(1)

    BEST USE: Short documents, single keyword searches
    """
        elif results_list[0]['algorithm'] == "Rabin-Karp":
            details += """
    🔹 RABIN-KARP ALGORITHM
    ────────────────────────────────────────────────────────────────────

    DESCRIPTION:
    • Uses rolling hash function for pattern matching
    • Computes hash values and compares them
    • Only does character comparison when hashes match

    TIME COMPLEXITY: O(n + m) average case
    SPACE COMPLEXITY: O(1)

    BEST USE: Multiple keyword matching, large documents
    """
        else:
            details += """
    🔹 KMP (KNUTH-MORRIS-PRATT) ALGORITHM
    ────────────────────────────────────────────────────────────────────

    DESCRIPTION:
    • Uses preprocessing to build failure function (LPS array)
    • Never backtracks in the main text
    • Skips unnecessary comparisons intelligently

    TIME COMPLEXITY: O(n + m) - Guaranteed!
    SPACE COMPLEXITY: O(m)

    BEST USE: Production systems, large CV documents
    """
        
        details += """

    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                  🏆 ALGORITHM COMPARISON 🏆                          ║
    ╚═══════════════════════════════════════════════════════════════════════╝

    ALGORITHM      | TIME          | SPACE | BEST FOR
    ───────────────┼───────────────┼───────┼─────────────────────
    Brute Force    | O(n × m)      | O(1)  | Small texts
    Rabin-Karp     | O(n+m) avg    | O(1)  | Multiple patterns
    KMP            | O(n+m)        | O(m)  | Long patterns

    ═══════════════════════════════════════════════════════════════════════
                Batch Analysis Complete! 
    ═══════════════════════════════════════════════════════════════════════
    """
        
        self.details_text.setText(details)
    
    def view_candidate_details(self, item):
        """View detailed analysis when double-clicking a candidate"""
        row = item.row()
        filename = self.ranking_table.item(row, 1).text()
        
        self.show_styled_message("Candidate Details", 
            f" {filename}\n\n"
            f"To view full analysis:\n"
            f"1. Click 'Browse CV'\n"
            f"2. Select this file\n"
            f"3. Click 'ANALYZE CV'", 
            "success")


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = CVAnalyzerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
           