#!/usr/bin/python
''' Hamerkop - A simple static site generator written in python for bencane.com '''

import mistune
import jinja2
import argparse
import yaml
import os
import sys
from datetime import datetime
from distutils import dir_util



def load_post_config(config):
    ''' Find article yml files and load them into metadata dictionary '''
    metadata = {}
    dir_contents = os.listdir(config['articles']['config'])
    for item in dir_contents:
        fullpath = config['articles']['config'] + "/" + item
        if os.path.isfile(fullpath):
            afh = open(fullpath, "r")
            meta = yaml.safe_load(afh)
            afh.close()
            metadata[meta['post_id']] = meta
    return metadata


def get_post_data(filename):
    ''' Grab the post written in markdown and parse into HTML'''
    markdown = mistune.Markdown()
    pfh = open(filename, "r")
    data = pfh.read()
    pfh.close()
    return markdown(data)


def render_page(data, meta, template, template_path):
    ''' Take post or fulldata and generate HTML page '''
    template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    template_env = jinja2.Environment(loader=template_loader)
    template_obj = template_env.get_template(template)
    template_vars = {
        'data' : data,
        'meta' : meta,
    }
    return template_obj.render(template_vars)


def create_page(path, filename, content):
    ''' Take a filename as input and create a file '''
    if not os.path.isdir(path):
        os.makedirs(path)
    filename_path = path + "/" + filename
    try:
        fh = open(filename_path, "w")
        fh.write(content)
        fh.close()
        return True
    except:
        return False


if __name__ == "__main__":
    # Grab commandline arguments and process them
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="Specify a configuration file",
                        required=True)
    args = parser.parse_args()

    # Open specified config file and load as yaml or error
    try:
        cfh = open(args.config, "r")
    except:
        sys.stderr.write("Could not open file: {0}\n".format(args.config))
        sys.exit(1)
    config = yaml.safe_load(cfh)
    cfh.close()

    # Define fulldata with all article metadata
    fulldata = load_post_config(config)

    # Grab article data and start generating pages
    for post in fulldata.keys():
        filename = config['articles']['posts'] + "/" + fulldata[post]['file']
        fulldata[post]['data'] = get_post_data(filename)

        # Generate article specific settings
        meta = config
        meta['page_type'] = "article"

        # Place a copy in each level for backwards capatability
        slug = fulldata[post]['slug']
        slugs = []
        slugs.append(config['output_dir'] + datetime.strftime(fulldata[post]['date'],
                                                              '/%Y/%m/%d/') + slug)
        slugs.append(config['output_dir'] + datetime.strftime(fulldata[post]['date'],
                                                              '/%Y/%m/') + slug)
        slugs.append(config['output_dir'] + datetime.strftime(fulldata[post]['date'],
                                                              '/%Y/') + slug)
        # Define a full_url key for each post
        fulldata[post]['full_url'] = datetime.strftime(fulldata[post]['date'], '/%Y/%m/%d/') + slug + "/"

        # While grabbing data generate static articles
        rendered_page = render_page(fulldata[post],
                                    config,
                                    config['templates']['article'],
                                    config['template_dir'])

        # Start creatin article pages
        data = rendered_page
        if fulldata[post]['published']:
            for slug_path in slugs:
                if create_page(slug_path, "index.html", data):
                    print "Successfully created file {0}".format(slug_path)
                else:
                    print "Error creating article {0}".format(slug_path)
        else:
            fulldata.pop(post, None)
            print "Skipping article {0} as it has not been published yet".format(post)

    # Create additional pages defined in config
    for page in config['additional_pages'].keys():
        meta = config
        meta['page_type'] = page
        meta['post_ids'] = fulldata.keys()

        # Ensure additional paths are added if required
        if "add_path" in config['additional_pages'][page]:
            output_dir = config['output_dir'] + "/" + config['additional_pages'][page]['add_path']
        else:
            output_dir = config['output_dir']

        # Render page and create it
        rendered_page = render_page(fulldata,
                                    meta,
                                    config['templates'][page],
                                    config['template_dir'])
        created_file = "{0}/{1}".format(output_dir, config['additional_pages'][page]['url'])
        if create_page(output_dir, config['additional_pages'][page]['url'], rendered_page):
            print "Successfully created file {0}".format(created_file)
        else:
            print "Error creating article {0}".format(created_file)

    # Copy static files at the end
    dir_util.copy_tree(config['static_dir'], config['output_dir'] + "/static")
