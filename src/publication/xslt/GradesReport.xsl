<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exslt="http://exslt.org/common"
  extension-element-prefixes="exslt">

  <xsl:output method="html" doctype-system="about:legacy-compat" encoding="UTF-8" indent="yes" />

  <!-- Paramètres -->
  <xsl:param name="moduleFilter" select="'GINF35 administration et programmation sys'" />

  <!-- Clé pour le groupement par code_apogee et ModuleName -->
  <xsl:key name="student-module" match="Notes" use="concat(code_apogee, '|', ModuleName)" />

  <xsl:template match="/Root">
    <html>
      <head>
        <title>Grades Report for Specific Module</title>
        <style>
          .red { background-color: #f8d7da; }
          .orange { background-color: #fff3cd; }
          .green { background-color: #d4edda; }
          table { border-collapse: collapse; width: 100%; }
          th, td { padding: 8px 12px; border: 1px solid #ddd; text-align: left; }
          th { background-color: #f2f2f2; }
        </style>
      </head>
      <body>
        <h1>Grades Report for Module: <xsl:value-of select="$moduleFilter" /></h1>
        <table>
          <tr>
            <th>Student Name</th>
            <th>Module Name</th>
            <th>Element Name</th>
            <th>Grade</th>
            <th>Average Grade</th>
          </tr>

          <!-- Itérer sur chaque groupe unique de code_apogee et ModuleName -->
          <xsl:for-each
            select="Notes[ModuleName = $moduleFilter][generate-id() = generate-id(key('student-module', concat(code_apogee, '|', ModuleName))[1])]">
            <xsl:variable name="currentGroup"
              select="key('student-module', concat(code_apogee, '|', ModuleName))" />
            <xsl:variable name="sumGrades" select="sum($currentGroup/Grade)" />
            <xsl:variable name="countGrades" select="count($currentGroup/Grade)" />
            <xsl:variable name="average" select="$sumGrades div $countGrades" />

            <!-- Définir la classe CSS basée sur la moyenne -->
            <xsl:variable name="gradeClass">
              <xsl:choose>
                <xsl:when test="$average &lt; 8">red</xsl:when>
                <xsl:when test="$average &gt;= 8 and $average &lt; 12">orange</xsl:when>
                <xsl:otherwise>green</xsl:otherwise>
              </xsl:choose>
            </xsl:variable>

            <!-- Obtenir le nom de l'étudiant (Nom seulement) -->
            <xsl:variable name="studentID" select="code_apogee" />
            <xsl:variable name="studentName">
              <xsl:for-each
                select="document('file:///C:/Users/utente/XmlProject/data/output/xml/Students_GInf2.xml')/Root/Students[code_apogee = $studentID]">
                <xsl:value-of select="concat(Nom, ' ', Prenom)" />
              </xsl:for-each>
            </xsl:variable>


            <!-- Itérer sur chaque note dans le groupe -->
            <xsl:for-each select="$currentGroup">
              <tr>
                <!-- Afficher le nom de l'étudiant et le nom du module une seule fois -->
                <xsl:if test="position() = 1">
                  <td rowspan="{count($currentGroup)}">
                    <xsl:value-of select="$studentName" />
                  </td>
                  <td rowspan="{count($currentGroup)}">
                    <xsl:value-of select="ModuleName" />
                  </td>
                </xsl:if>

                <!-- Afficher le nom de l'élément et la note -->
                <td>
                  <xsl:value-of select="ElementName" />
                </td>
                <td>
                  <xsl:value-of select="Grade" />
                </td>

                <!-- Afficher la moyenne dans la première ligne du groupe -->
                <xsl:if test="position() = 1">
                  <td rowspan="{count($currentGroup)}" class="{ $gradeClass }">
                    <xsl:value-of select="format-number($average, '0.00')" />
                  </td>
                </xsl:if>
              </tr>
            </xsl:for-each>

          </xsl:for-each>

        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>