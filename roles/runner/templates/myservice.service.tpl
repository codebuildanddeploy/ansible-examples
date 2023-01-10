[Unit]
Description=Demo service

[Service]
User={{ service_automation_user }}
Group={{ service_automation_group | default(service_automation_user) }}
ExecStart={{ service_install_folder }}/{{ service_name }}

[Install]
WantedBy=multi-user.target