import zc.metarecipe
import zc.zk

class Recipe(zc.metarecipe.Recipe):

    def __init__(self, buildout, name, options):

        super(Recipe, self).__init__(buildout, name, options)

        assert name.endswith('.0'), name # There can be only one.
        name = name[:-2]

        zk = self.zk = zc.zk.ZK('zookeeper:2181')

        path = '/' + name.replace(',', '/')
        zkoptions = zk.properties(path, False)

        user = zkoptions.get('user', 'zope')
        dsn = zkoptions.get('dsn')
        command = str(zkoptions['command'])
        if dsn:
            prefix = 'SENTRY_DSN=%s\n' % dsn
            command = "/opt/zkcron/bin/raven_cron %r" % command
        else:
            prefix = ''

        self['deployment'] = dict(
            recipe = 'zc.recipe.deployment',
            name=name,
            user=user,
            )

        text = "%(schedule)s %(user)s %(command)s\n#\n" % dict(
            user = user,
            command = command,
            schedule = zkoptions['schedule'],
            )

        self[name] = dict(
            recipe = 'zc.recipe.deployment:configuration',
            deployment = 'deployment',
            text = prefix + text,
            directory = "/etc/cron.d",
            )
