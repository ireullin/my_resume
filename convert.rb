require 'yaml'

def main

    data = YAML.load_file("resume.yaml")
    data['attainments']['items'].each do |r|
        p r['summary']['zh']
    end
end

main if $0==__FILE__

