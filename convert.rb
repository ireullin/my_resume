require 'yaml'

def main

    p YAML.load_file("resume.yaml")
end

main if $0==__FILE__

