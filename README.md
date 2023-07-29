# Hardcoded Fingerprint comma.ai openpilot Installer Helper

## How and Why to use

openpilot configures itself to your vehicle by using a fingerprint of firmwares on your vehicle.

Please make sure you understand what [Fingerprinting](https://github.com/commaai/openpilot/wiki/Fingerprinting) is. If you get `Car Unrecognized: Dashcam Mode`, you should try to go through that guide. If you are still having trouble going through the guide, you can use this repository to install openpilot on your vehicle with a hardcoded fingerprint. _Be aware that an erronous fingerprint can cause your vehicle and openpilot to behave unexpectedly_. Please note that this repository is not a replacement for proper fingerprinting and should only be used as a last and temporary resort.

This GitHub repository continuously generates openpilot branches off of "stable" `release3` and "unstable" `master-ci` with hardcoded fingerprints for the purpose of installing comma.ai openpilot on un-fingerprinted vehicles where there is currently trouble or blocks upstreaming fingerprints or there is currently a massive lag in fingerprints of the  "stable" `release3` compared to the "unstable" `master-ci` that has more fingerprints.

The branches here should be considered a temporary solution until the official openpilot repository is updated with the necessary fingerprints for either "stable" `release3` or "unstable" `master-ci`. At which point, users should switch back to the official openpilot branches of the stable `release3` or "unstable" `master-ci`.

You can see and search the branches generated by this repository here:

https://github.com/hardcoded-fp/openpilot/branches

Let's do an example.

Say you have a "HYUNDAI SANTA FE HYBRID 2022", but it's not fingerprinted in comma's `release3` branch for whatever reason and currently shows `Car Unrecognized: Dashcam Mode`. At the time of this README, Hyundai is going through some sort of firmware interrogation overhaul so upstreaming fingerprints is a bit blocked. With this repository, you would find the corresponding branch in the [branch list](https://github.com/hardcoded-fp/openpilot/branches). In this case, the corresponding branch is `hyundai_santa_fe_hybrid_2022`.

Then construct the following URL for the [URL installer](https://github.com/commaai/openpilot/wiki/Forks#url-installers-at-installation-screen) that you can enter into your comma device and enter it in as "Custom Software" on the installation screen:

https://installer.comma.ai/hardcoded-fp/release3-hyundai_santa_fe_hybrid_2022

If all goes well, you'll run through the installation process and have "stable" `release3` openpilot installed on your vehicle with a hardcoded fingerprint. Please note that this is a hack and while this change may be a small change upon `release3`, it is not officially supported by comma.ai. You should switch back to the official openpilot branches of the corresponding base branch when you can.

## Custom Forks

This is generally not necessary for other forks as many of them have vehicle selectors. This is only useful for openpilot codebases without selectors such as comma's official openpilot.

## Why not dynamically generate the installer and inject the fingerprint?

Injecting the fingerprint with the installer may produce orphaned commits or non-commited code that can only be found on the device itself. By producing these branches periodically with GitHub, the commit on the device will have a commit in GitHub that can be referenced if help is sought.
