# toil_cvflag

[![pypi badge][pypi_badge]][pypi_base]
[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]
[![docker badge][docker_badge]][docker_base]
[![docker badge][automated_badge]][docker_base]

A toil implementation of caveman flagging for vcf files.

![toil_cvflag](https://user-images.githubusercontent.com/7906289/51571952-d9756d00-1e71-11e9-8274-f5bf90fe8558.png)

## Usage

This package uses docker to manage its dependencies, there are 2 ways of using it:

1. Running the [container][docker_base] in single machine mode without [`--batchSystem`] support:

        # using docker
        docker run -it papaemmelab/toil_cvflag --help

        # using singularity
        singularity run docker://papaemmelab/toil_cvflag --help

1. Installing the python package from [pypi][pypi_base] and passing the container as a flag:

        # install package
        pip install toil_cvflag

        # run with docker
        toil_cvflag [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --docker papaemmelab/toil_cvflag
            --volumes <local path> <container path>
            --batchSystem LSF

        # run with singularity
        toil_cvflag [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --singularity docker://papaemmelab/toil_cvflag
            --volumes <local path> <container path>
            --batchSystem LSF

See [docker2singularity] if you want to use a [singularity] image instead of using the `docker://` prefix.

## Options

The following options are required to run caveman postprocessing:

| Option            | Description                             |
| ----------- | --------------------------------------------- |
| --vcf             | Path to input vcf file                  |
| --out             | Path to caveman flagged output vcf file |
| --normal-bam      | Path to normal bam                      |
| --tumor-bam       | Path to tumor bam                       |
| --bedFileLoc      | Path to a folder containing centromeric, snp, hi seq depth, simple repeat bed files |
| --indelBed        | A bed file containing germline indels to filter on |
| --unmatchedVCFLoc | Path to folder containing unmatched VCF PON |
| --annoBedLoc      | Path to bed files containing annotatable regions and coding regions |
| --sequencing-method   | WGS or TGD |
| --bin-size        | Number of variants to split the vcf to parallelize flagging (default: 100000) |

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

This package was created using [Cookiecutter] and the
[papaemmelab/cookiecutter-toil] project template.

<!-- References -->
[singularity]: http://singularity.lbl.gov/
[docker2singularity]: https://github.com/singularityware/docker2singularity
[cookiecutter]: https://github.com/audreyr/cookiecutter
[papaemmelab/cookiecutter-toil]: https://github.com/papaemmelab/cookiecutter-toil
[`--batchSystem`]: http://toil.readthedocs.io/en/latest/developingWorkflows/batchSystem.html?highlight=BatchSystem

<!-- Badges -->
[docker_base]: https://hub.docker.com/r/papaemmelab/toil_cvflag
[docker_badge]: https://img.shields.io/docker/cloud/build/papaemmelab/toil_cvflag.svg
[automated_badge]: https://img.shields.io/docker/cloud/automated/papaemmelab/toil_cvflag.svg
[codecov_badge]: https://codecov.io/gh/papaemmelab/toil_cvflag/branch/master/graph/badge.svg
[codecov_base]: https://codecov.io/gh/papaemmelab/toil_cvflag
[pypi_badge]: https://img.shields.io/pypi/v/toil_cvflag.svg
[pypi_base]: https://pypi.python.org/pypi/toil_cvflag
[travis_badge]: https://img.shields.io/travis/papaemmelab/toil_cvflag.svg
[travis_base]: https://travis-ci.org/papaemmelab/toil_cvflag
