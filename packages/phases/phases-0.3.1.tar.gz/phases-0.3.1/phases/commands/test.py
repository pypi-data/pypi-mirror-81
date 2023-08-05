"""
Test a Project
"""

from unittest.result import TestResult
from pyPhases.test import TestCase, TestCaseIntegration
from unittest.loader import TestLoader
from unittest.suite import TestSuite
from unittest import TextTestRunner
from .run import Run
import os
import sys


class Test(Run):
    """test a Phase-Project by wrapping TestCases from pyPhase with the project and a configfile specified in project.test.yaml"""

    testDir = "tests"
    testPattern = "test*.py"

    def parseRunOptions(self):
        super().parseRunOptions()
        if self.options["<testdir>"]:
            self.testDir = os.path.join(self.outputDir, self.options["<testdir>"])
            sys.path.insert(0, self.testDir)
            self.logDebug("Set Testdir: %s" % (self.testDir))
        if self.options["<testpattern>"]:
            self.testPattern = self.options["<testpattern>"]
        if self.options["-c"] is None:
            self.projectConfigFileName = os.path.join(self.outputDir, "project.test.yaml")
            self.logDebug("Set Config file: %s" % (self.projectFileName))

    def wrapTestsInSuite(self, testOrSuite, wrapMethod):
        tests = []
        if issubclass(type(testOrSuite), TestSuite):
            for subTestOrSuite in testOrSuite._tests:
                tests += self.wrapTestsInSuite(subTestOrSuite, wrapMethod)
        else:
            check = wrapMethod(testOrSuite)
            if check:
                tests = [testOrSuite]
        return tests

    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)

        loader = TestLoader()
        self.logDebug("Discover Tests in %s for pattern %s (Basedir: %s)" % (self.testDir, self.testPattern, self.outputDir))
        os.chdir(self.outputDir)
        suite = loader.discover(self.testDir, self.testPattern)
        self.logDebug("Found Tests: %s" % (suite._tests))

        def wrapTestsInSuite(test):
            if isinstance(test, TestCaseIntegration):
                return False
            if isinstance(test, TestCase):
                test.setProject()
            return True

        TestCase.project = project
        noIntegrationTests = self.wrapTestsInSuite(suite, wrapTestsInSuite)

        suite = TestSuite()
        suite.addTests(noIntegrationTests)
        runner = TextTestRunner()
        return runner.run(suite)
