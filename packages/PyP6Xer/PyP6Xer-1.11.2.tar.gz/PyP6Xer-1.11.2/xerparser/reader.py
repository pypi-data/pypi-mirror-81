'''
This file starts the process of reading and parsing xer files

'''
import csv
import mmap
from tqdm import tqdm

from xerparser import *


class Reader:

    current_table = ''
    current_headers = []

    def create_object(self, object_type, params):
        """

        Args:
            object_type:
            params:

        Returns:

        """
        if object_type.strip() == "CURRTYPE":
            self._currencies.add(params)
        elif object_type.strip() == "ROLES":
            self._roles.add(params)
        elif object_type.strip() == "ACCOUNT":
            self._accounts.add(params)
        elif object_type.strip() == "ROLERATE":
            self._rolerates.add(params)
        elif object_type.strip() == "OBS":
            self._obss.add(params)
        elif object_type.strip() == "RCATTYPE":
            self._rcattypes.add(params)
        elif object_type.strip() == "UDFTYPE":
            self._udftypes.add(params)
        elif object_type.strip() == "RCATVAL":
            self._rcatvals.add(params)
        elif object_type.strip() == "PROJECT":
            self._projects.add(params)
        elif object_type.strip() == "CALENDAR":
            self._calendars.add(params)
        elif object_type.strip() == "SCHEDOPTIONS":
            self._schedoptions.add(params)
        elif object_type.strip() == "PROJWBS":
            self._wbss.add(params)
        elif object_type.strip() == "RSRC":
            self._resources.add(params)
        elif object_type.strip() == "RSRCCURV":
            self._rsrcurves.add(params)
        elif object_type.strip() == "ACTVTYPE":
            self._acttypes.add(params)
        elif object_type.strip() == "RSRCRATE":
            self._rsrcrates.add(params)
        elif object_type.strip() == "RSRCRCAT":
            self._rsrccats.add(params)
        elif object_type.strip() == "TASK":
            self._tasks.add(params)
        elif object_type.strip() == "ACTVCODE":
            self._activitycodes.add(params)
        elif object_type.strip() == "TASKPRED":
            self._predecessors.add(params)
        elif object_type.strip() == "TASKRSRC":
            self._activityresources.add(params)
        elif object_type.strip() == "TASKACTV":
            self._activitycodes.add(params)
        elif object_type.strip() == "UDFVALUE":
            self._udfvalues.add(params)

    def summary(self):
        print('Number of activities: ', self.tasks.count)
        print('Number of relationships: ', len(TaskPred.obj_list))

    @property
    def projects(self):
        """
        Projects

        Returns: list of all projects contained in the xer file

        """
        return self._projects

    @property
    def tasks(self):
        return self._tasks

    @property
    def wbss(self):
        return self._wbss

    @property
    def relations(self):
        return self._predecessors

    @property
    def resources(self):
        return self._resources

    @property
    def accounts(self):
        return self._accounts

    @property
    def activitycodes(self):
        return self._activitycodes

    @property
    def acttypes(self):
        return self._acttypes

    @property
    def calendars(self):
        return self._calendars

    @property
    def currencies(self):
        return self._currencies

    @property
    def obss(self):
        return self._obss
    @property
    def rcattypes(self):
        return self.rcattypes

    @property
    def rcatvals(self):
        return self._rcatvals

    @property
    def rolerates(self):
        return self._rolerates

    @property
    def roles(self):
        return self._roles

    @property
    def resourcecurves(self):
        return self._rsrcurves

    @property
    def resourcerates(self):
        return self._rsrcrates

    @property
    def resourcecategories(self):
        return self._rsrccats

    @property
    def scheduleoptions(self):
        return self._schedoptions

    @property
    def activityresources(self):
        return self._activityresources

    @property
    def udfvalues(self):
        return self._udfvalues

    @property
    def udftypes(self):
        return self._udftypes

    def __init__(self, filename):
        file = open(filename, 'r')
        self._tasks = Tasks()
        self._predecessors = Predecessors()
        self._projects = Projects()
        self._wbss = WBSs()
        self._resources = Resources()
        self._accounts = Accounts()
        self._activitycodes = ActivityCodes()
        self._acttypes = ActTypes()
        self._calendars = Calendars()
        self._currencies = Currencies()
        self._obss = OBSs()
        self._rcatvals = RCatVals()
        self._rcattypes = RCatTypes()
        self._rolerates = RoleRates()
        self._roles = Roles()
        self._rsrcurves = ResourceCurves()
        self._rsrcrates = ResourceRates()
        self._rsrccats = ResourceCategories()
        self._schedoptions = SchedOptions()
        self._activityresources = ActivityResources()
        self._udftypes = UDFTypes()
        self._udfvalues = UDFValues()
        with open(filename) as tsvfile:
            stream = csv.reader(tsvfile, delimiter='\t')
            #for row in stream:
            for row in tqdm(stream, total=self.get_num_lines(filename)):
                if row[0] =="%T":
                    current_table = row[1]
                elif row[0] == "%F":
                    current_headers = [r.strip() for r in row[1:]]
                elif row[0] == "%R":
                    zipped_record = dict(zip(current_headers, row[1:]))
                    self.create_object(current_table, zipped_record)

        # for line in content:
        #     line_lst = line.split('\t')
        #     if line_lst[0] == "%T":
        #         current_table = line_lst[1]
        #     elif line_lst[0] == "%R":
        #         self.create_object(current_table, line_lst[1:])

    def get_num_lines(self, file_path):
        fp = open(file_path, "r+")
        buf = mmap.mmap(fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines
