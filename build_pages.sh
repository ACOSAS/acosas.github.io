#!/usr/bin/env ruby

require 'acos_jekyll_openapi'

@pwd = Dir.pwd

puts "current dir: %s" % @pwd

AcosOpenApiHelper.generate_pages_from_data(
    "%s/_data/swagger" % @pwd, 
    "%s" % @pwd,
    "%s/pages/swagger" % @pwd
)