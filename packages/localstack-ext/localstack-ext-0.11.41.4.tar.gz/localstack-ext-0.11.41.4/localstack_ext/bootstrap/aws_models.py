from localstack.utils.aws import aws_models
FVytA=super
FVyth=None
FVytz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  FVytA(LambdaLayer,self).__init__(arn)
  self.cwd=FVyth
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,FVytz,env=FVyth):
  FVytA(RDSDatabase,self).__init__(FVytz,env=env)
 def name(self):
  return self.FVytz.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,FVytz,env=FVyth):
  FVytA(RDSCluster,self).__init__(FVytz,env=env)
 def name(self):
  return self.FVytz.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
