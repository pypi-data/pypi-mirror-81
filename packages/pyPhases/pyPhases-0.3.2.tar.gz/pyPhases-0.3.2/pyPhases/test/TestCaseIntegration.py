from pyPhases.test.TestCase import TestCase


class TestCaseIntegration(TestCase):
    def setUp(self):
        self.beforePrepare()
        super().setUp()
        self.beforeRun()
        self.phase.run()
        self.afterRun()

    def beforePrepare(self):
        pass

    def beforeRun(self):
        pass

    def afterRun(self):
        pass
