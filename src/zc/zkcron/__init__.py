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

        self['deployment'] = dict(
            recipe = 'zc.recipe.deployment',
            name=name,
            user=user,
            )

        self[name] = dict(
            recipe = 'zc.recipe.deployment:configuration',
            deployment = 'deployment',
            text = "%(schedule)s %(user)s %(command)s\n" % dict(
                user = user,
                command = zkoptions['command'],
                schedule = zkoptions['schedule'],
                ),
            directory = "/etc/cron.d",
            )
