<div align="center">
<a class="badge" href="https://github.com/fulso-me/cdhelm"><img src="https://img.shields.io/badge/-Github-blue" alt="Github"></a>
<a class="badge" href="https://pypi.org/project/cdhelm/"><img src="https://img.shields.io/badge/-PyPI-blue" alt="PyPI"></a>
</div>

# Why

I still have two fundamental problems with using helm now that tiller is gone.
The first is that it sometimes requires you to put secrets in config files.
There's no good universal way to specify my manifests with shared secrets
without having them show up in my repositories. The second is that there's no
good way to manage global variables within a massive project. Sure it's
possible with subcharts, but I've found it gets really messy really quickly.

I like using cdk8s for my own images and deployments. I think it's clean and
easy way to follow best practices, and with the help of jedi and autocompletion
it's super easy to write things that you know will work right.

# Installing

`pipenv install cdhelm` to add cdhelm to your Pipfile.

`from cdhelm import Helm` in your cdk8s file.

# Workflow

This library allows you to specify a helm chart within cdk8s. It's pretty
flexible with how it lets you organize your project. 

You can define a Helm object like so:

``` python
prometheus = Helm(
    name="prometheus",
    repo="https://kubernetes-charts.storage.googleapis.com",
    chart="prometheus",
    version="11.12.0",
    namespace="monitoring,
    path=".charts",
)
```

`namespace` defaults to `default` and `path` defaults to `.charts`. Otherwise
everything else is required. `version` is explicitly required because I can't
think of a reason you should ever rely on `latest` implicitly.

This returns a Helm object that you can interact with. Creating the object
pulls the chart to `path` and populates `object.values` with the default values
file. The is currently no option to not pull the whole chart.

## Adding values

You can specify new values either through a values file like with normal helm charts.

``` python
prometheus.updateFile("configs/prometheus.yaml")
```

Or you can specify new values through a python dictionary corrisponding to the values file.


``` python
prometheus_conf = {
    "alertmanager": {
        "baseURL": "https://alert." + mydomain
    },
    "server": {
        "baseURL": "https://prom." + mydomain
    },
}
prometheus.update(prometheus_conf)
```

Both actions only update exactly what is specified so it's possible to use both
together even on variables within the same scope.

## Extracting values or working entirely within cdk8s

It is possible to create a cdk8s chart from the Helm object. This chart will
bake in the current values. Please update your values before returning a chart.

``` python
monitoring_app = App(outdir=dist + "monitoring")
prometheus_chart = prometheus.Chart(monitoring_app, "prometheus")
```

You can use this to pass along information from the chart such as services and
ports to other parts of your code. This is a good way to interface different
parts of your server without hardcoding values. You may synth the app the chart
is a part of and work with helm as though it's just another part of your cdk8s
implementation. Every part of the chart will be rendered out using `helm template`.

``` python
monitoring_app.synth()
```

## Working outside of cdk8s

It is also possible to keep the benefits of having helm specified in your cdk8s
code while still letting helm do its thing. You can have cdk8s write out a
`values.yaml` file so you can manage helm manually.  `render()` will overwrite
the default rendered values path.

``` python
prometheus.render("helm/myvalues.yaml")
```

Or you can have cdk8s render out a helper script to the specified folder to
work with exactly the version and values you already specified.

``` python
prometheus.write_controls("_charts")
```

The rendered script should work with any helm command that works with a
specific chart. Use `-h` with the chart to see a help printout.

```
All commands will be given the following options when applicable:
  --namespace monitoring
  --repo https://kubernetes-charts.storage.googleapis.com
  --version 11.12.0
  --values /home/myhome/myproject/.charts/prometheus-11.12.0/prometheus/rendered-values.yaml
  [NAME] => prometheus
  [CHART] => prometheus
  [RELEASE] => prometheus

All other given options will be appended
Use -h as an appended option for any helm command

Available Helm commands:
  help
  history
  install
  rollback
  show all
  show chart
  show readme
  show values
  status
  template
  test
  uninstall
  upgrade

```
