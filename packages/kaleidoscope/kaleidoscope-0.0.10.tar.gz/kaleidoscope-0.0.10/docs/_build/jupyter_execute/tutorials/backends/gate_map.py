from qiskit import IBMQ
IBMQ.load_account()
from kaleidoscope.qiskit.backends.interactive import system_gate_map

pro = IBMQ.get_provider(group='open')
backend = pro.backends.ibmq_vigo
system_gate_map(backend)

system_gate_map(backend, qubit_labels=['A', 'B', 'C', 'D', 'E'])

system_gate_map(backend,
             qubit_labels=['A', 'B', 'C', 'D', 'E'],
             qubit_colors='#8b7b8b')

system_gate_map(backend,
             qubit_labels=['A', 'B', 'C', 'D', 'E'],
             qubit_colors=['#8b7b8b', '#845e49', '#496b3a', '#e97fa5', '#ff9999'])

system_gate_map(backend,
             qubit_colors='#8b7b8b',
             line_colors='#ff9999')

system_gate_map(backend,
             line_colors=['#845e49', '#496b3a', '#e97fa5', '#ff9999']*2)

system_gate_map(backend, label_qubits=False)

system_gate_map(backend,
                qubit_colors='white',
                font_color="black",
                line_colors='white',
                background_color='black')