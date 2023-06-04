# Purpose of the folder
Provide utility classes for main.py, setup/ and other folders

# File purposes
<ul>
    <li><code>__init__.py</code></li>
    imports modules to run the program
    <li><code>data_classes.py</code></li>
    Provides the implementation of <code>Question</code>,<code>CustomQuestion</code>, and <code>UserInfo</code> classes which are used elsewhere in the code
    <li><code>generic.py</code></li>
    Home to the <code>UseLogger</code> class, which defines a <code>__init__</code> method that requires a logger, as well as the <code>FileHandler</code> class, which is used for QOL improvements when working with old diagnosis results. It also contains the <code>set_theme</code> function, which sets the appearance theme of the program at runtime.
    <li><code>mcq.py</code></li>
    Home to the <code>MCQBuilder</code> class, which is the implementation behind all quizzes in the program
    <li><code>special.py</code></li>
    Home to all "special" things, like the Health Log, Settings, and Medicine. Migration to this file is still a work in progress
    <li><code>parse_json.py</code></li>
    QOL improvements when accessing and working with <code>json</code> files.
</ul>
