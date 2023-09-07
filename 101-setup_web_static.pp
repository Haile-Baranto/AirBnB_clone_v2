#!/usr/bin/puppet apply
exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

exec { 'remove-current':
  command => 'rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get-update'],
}

file { ['/var/www', '/var/www/html/index.html', '/var/www/error/404.html']:
  ensure  => present,
  mode    => '0755',
  recurse => true,
  require => Package['nginx'],
}

file { '/var/www/html/index.html':
  content => 'Hello, World!',
}

file { '/var/www/error/404.html':
  content => "Ceci n'est pas une page",
}

file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure  => directory,
  require => Package['nginx'],
}

file { '/data/web_static/releases/test/index.html':
  content =>
"<!DOCTYPE html>
<html lang='en-US'>
	<head>
		<title>Home - AirBnB Clone</title>
	</head>
	<body>
		<h1>Welcome to AirBnB!</h1>
	<body>
</html>
",
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file_line { 'nginx_config':
  path    => '/etc/nginx/sites-available/default',
  line    => "\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  after   => "\tlocation / {",
  require => Package['nginx'],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File_line['nginx_config'],
}