executarJupyter:
	jupyter-notebook
instalarDependenciasVirtualenv:
	sudo apt-get update
	sudo apt-get install python3.8-venv
	sudo apt-get install python3.8-tk
criarAmbienteVirtualenv:
	python3.8 -m venv AmbienteTP
	AmbienteTP/bin/pip3.8 install --upgrade pip
	AmbienteTP/bin/pip3.8 install -r requirements.txt
	clear
	echo "Pacotes instalados:"
	AmbienteTP/bin/pip3.8 freeze
atualizarAmbienteVirtualenv:
	AmbienteTP/bin/pip3.8 install --upgrade pip
	AmbienteTP/bin/pip3.8 install -r requirements.txt
removerAmbienteVirtualenv:
	rm -r AmbienteTP/
temaMonokaiJupyter:
	jt -t monokai -f fira -fs 11 -nf ptsans -nfs 13 -N -kl -cursw 2 -cursc r -cellw 95% -T
	# Documentação: https://github.com/dunovank/jupyter-themes
	# Opções de temas:
	# onedork
	# grade3
	# oceans16
	# chesterish
	# monokai
	# solarizedl
	# solarizedd