import ablauf.apmn


# State classes
# ============================================================================
# init state
# ****************************************************************************
class Init(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)
