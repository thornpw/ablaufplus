from distutils.core import setup

setup(
        name='ablauf',
        version='0.1.7',
        license="GNU LGPLv3",
        description='A state machine implemented in python. Uses states and transitions. Enhanced wiht a MVC layer. The controllers are inspired by BPMN.',
        long_description=open("README.txt").read(),
        author='Thorsten Butschke',
        author_email='thorsten.butschke@googlemail.com',
        url='https://github.com/thornpw/ablaufplus',
        packages=['ablauf'],
        package_dir={'ablauf': 'src/ablauf'},
        package_data={
            'ablauf': [
                'docs/*.*',
                'ablaufed/*.*',
                'ablaufed/examples/*.*',
                'ablaufed/ablaufpad/*.*',
                'ablaufed/ablaufpad/templates/*.*',
                'ablaufed/ablaufpad/templates/Input_handler/*.*',
                'ablaufed/ablaufpad/templates/Input_handler/Stema/*.*',
                'ablaufed/ablaufpad/templates/Input_handler/Stema/configuration/*.*',
                'ablaufed/ablaufpad/templates/Input_handler/Stema/structure/*.*',
                'ablaufed/ablaufpad/templates/subcontroller/*.*',
                'ablaufed/ablaufpad/templates/subcontroller/dot/*.*',
                'ablaufed/ablaufpad/templates/subcontroller/views/*.*',
                'examples/*.*',
                'examples/Automate/*.*',
                'examples/Automate/configuration/*.*',
                'examples/Automate/processes/*.*',
                'examples/Automate/processes/App/*.*',
                'examples/simplegame/*.*',
                'examples/simplegame/configuration/*.*',
                'examples/simplegame/processes/*.*',
                'examples/simplegame/processes/App/*.*',
                'console_kernel/*.*',
                'pygamekern/*.*',
                'none_input_handler/*.*'
            ],
        },
        install_requires = [
            #"SQLAlchemy",
            #"jsonmerge",
            #"Jinja2"
        ],
        classifiers=[
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
        ]
)

