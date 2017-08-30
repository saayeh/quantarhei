In programs with a graphical user interface (GUI), you can often find a menu where you can configure your program´s behaviour. Quantarhei also provides means to configure its behaviour. Instead of a menu, there is a class called 'Manager' whose purpose is to allow modification of Quantarhei standard behaviour. Even such things as [[management of units|Management of units]] is handled by this class behind the scene.

The Manager class is a singleton. It only has one instance, and by multiple calls to its constructor you obtain one and the same object again (so we will call its instance "the manager" here). Most often you do not need to talk to the Manager class at all, but if you need to, this is the way to access is

    from quantarhei import Manager
    m = Manager()

The manager knows, for instance, what is the version of Quantarhei you use.

    print(m.version)

will return e.g.

    0.0.4

if you use the very early Quantarhei version 0.0.4.

### Manager's tasks

The manager handles the following tasks:
* Quantarhei configuration files in $HOME/.quantarhei directory
* Unit conversion and default units definition (see [[Management of Units|Management of Units]])
* Automatic basis conversion of certain quantum objects
* Plug-in registration and selection
* Project directory and file keeping

In future, the manager will also handle a GUI to enable a user friendly management of Quantarhei's set-up and plug-in and project management.

    