import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Tool

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Seed the database with 25 Infineon-style sample tools if it's empty
    if not Tool.query.first():
        sample_tools = [
            Tool(id='OSC-8392X', name='Tektronix 6 Series Oscilloscope', image_file='default.png', status='Available', location='Testing Bay A'),
            Tool(id='LOG-4491B', name='Keysight Logic Analyzer', image_file='default.png', status='Withdrawn', location='R&D Lab 2'),
            Tool(id='WAF-1102Q', name='Semi-Auto Wafer Prober', image_file='default.png', status='Calibration', location='Cleanroom 1'),
            Tool(id='THM-8823C', name='FLIR Thermal Imaging Camera', image_file='default.png', status='Available', location='Failure Analysis'),
            Tool(id='SPC-5512A', name='Rohde & Schwarz Spectrum Analyzer', image_file='default.png', status='Repair', location='RF Lab'),
            Tool(id='MIC-2219K', name='Leica Inspection Microscope', image_file='default.png', status='Available', location='Cleanroom 2'),
            Tool(id='SLD-9982Z', name='Weller High-Power Soldering Station', image_file='default.png', status='Withdrawn', location='Assembly Line B'),
            Tool(id='VNA-9932N', name='Vector Network Analyzer', image_file='default.png', status='Calibration', location='RF Lab'),
            Tool(id='SPA-4421P', name='Semiconductor Parameter Analyzer', image_file='default.png', status='Available', location='Failure Analysis'),
            Tool(id='ENV-5520C', name='Environmental Test Chamber', image_file='default.png', status='In Use', location='Reliability Lab'),
            Tool(id='SEM-8891M', name='Scanning Electron Microscope (SEM)', image_file='default.png', status='Available', location='Failure Analysis'),
            Tool(id='WIR-3321V', name='Ultrasonic Wire Bonder', image_file='default.png', status='Repair', location='Cleanroom 1'),
            Tool(id='MUL-7731M', name='Fluke 87V Digital Multimeter', image_file='default.png', status='Lost', location='Maintenance Hub'),
            Tool(id='SIG-9021Y', name='Arbitrary Waveform Generator', image_file='default.png', status='Available', location='Testing Bay A'),
            Tool(id='DIC-4410W', name='Automated Wafer Dicing Saw', image_file='default.png', status='Calibration', location='Cleanroom 2'),
            Tool(id='PWR-1105D', name='Programmable DC Power Supply', image_file='default.png', status='Withdrawn', location='R&D Lab 1'),
            Tool(id='AOI-5519O', name='Automated Optical Inspection (AOI)', image_file='default.png', status='Available', location='Assembly Line A'),
            Tool(id='FUM-8811H', name='Chemical Wet Bench / Fume Hood', image_file='default.png', status='Available', location='Wet Lab'),
            Tool(id='PLA-6612E', name='Plasma Etching System', image_file='default.png', status='Repair', location='Cleanroom 1'),
            Tool(id='ION-7734I', name='Ion Implanter Monitor', image_file='default.png', status='Withdrawn', location='Fab Bay 4'),
            Tool(id='DIE-3318A', name='High-Speed Die Attach Machine', image_file='default.png', status='Calibration', location='Assembly Line A'),
            Tool(id='OVN-2291U', name='UV Curing Conveyor Oven', image_file='default.png', status='Available', location='Assembly Line B'),
            Tool(id='ULT-6632C', name='Industrial Ultrasonic Cleaner', image_file='default.png', status='Available', location='Maintenance Hub'),
            Tool(id='WAF-8821S', name='Photoresist Wafer Spinner', image_file='default.png', status='Withdrawn', location='Cleanroom 2'),
            Tool(id='PHO-3329S', name='Photolithography Stepper Lens', image_file='default.png', status='Lost', location='Fab Bay 3')
        ]
        db.session.add_all(sample_tools)
        db.session.commit()

@app.route('/')
def dashboard():
    return render_template('catalog.html')

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/catalog')
def catalog():
    tools = Tool.query.all()
    counts = {
        'Total': len(tools),
        'Available': sum(1 for t in tools if t.status == 'Available'),
        'Withdrawn': sum(1 for t in tools if t.status == 'Withdrawn'),
        'Calibration': sum(1 for t in tools if t.status == 'Calibration'),
        'Repair': sum(1 for t in tools if t.status == 'Repair'),
        'Lost': sum(1 for t in tools if t.status == 'Lost')
    }
    
    # 2. Pass BOTH 'tools' and 'counts' to the HTML
    return render_template('catalog.html', tools=tools, counts=counts)

# --- NEW CRUD ROUTES ---

@app.route('/add', methods=['POST'])
def add_item():
    item_id = request.form.get('id')
    
    # Safety check: Prevent crashing if the user types an ID that already exists
    if Tool.query.get(item_id):
        return redirect(url_for('catalog')) # In a real app, you'd show a warning message here
        
    new_tool = Tool(
        id=item_id,
        name=request.form.get('name'),
        status=request.form.get('status'),
        location=request.form.get('location')
    )
    db.session.add(new_tool)
    db.session.commit()
    return redirect(url_for('catalog'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit_item(id):
    # Find the exact tool by its ID, update its fields, and save
    tool = Tool.query.get_or_404(id)
    tool.name = request.form.get('name')
    tool.status = request.form.get('status')
    tool.location = request.form.get('location')
    db.session.commit()
    return redirect(url_for('catalog'))

@app.route('/delete/<string:id>', methods=['POST'])
def delete_item(id):
    # Find the tool and remove it from the database
    tool = Tool.query.get_or_404(id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for('catalog'))

if __name__ == '__main__':
    app.run(debug=True)